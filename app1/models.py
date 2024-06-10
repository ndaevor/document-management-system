# models.py
from django.db import models
from django.contrib.auth.models import User
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import os
from Crypto.Util.Padding import pad, unpad
from django.core.files.storage import FileSystemStorage

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encryption_key = models.BinaryField(null=True, blank=True)
    iv = models.BinaryField(null=True, blank=True)
    file_hash = models.CharField(max_length=64, null=True, blank=True)  # Field to store the hash
    salt = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.file.name

    def encrypt_file(self, plaintext):
        # Pad the plaintext to ensure its length is a multiple of 16
        padded_plaintext = pad(plaintext, AES.block_size)
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(padded_plaintext)
        return base64.b64encode(ciphertext)

    def decrypt_file(self, ciphertext):
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, self.iv)
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        # Remove the padding after decryption
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data

    def compute_hash(self, data):
        # Combine data with salt and hash
        salted_data = self.salt.encode() + data
        return hashlib.sha256(data).hexdigest()

    def delete(self, *args, **kwargs):
        # Get the file path before deleting the instance
        storage = FileSystemStorage()
        file_path = self.file.path
        # Call the superclass delete method
        super().delete(*args, **kwargs)
        # Delete the file from the storage
        if storage.exists(file_path):
            storage.delete(file_path)
