from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Document
from .forms import DocumentForm 
from Crypto.Random import get_random_bytes
from django.core.files.base import ContentFile
import base64
from django.http import HttpResponse, JsonResponse
from haystack.query import SearchQuerySet

#check if user is sueruser --admin
def superuser_check(user):
    return user.is_superuser


#home
@login_required(login_url='login')
def HomePage(request):
    if superuser_check(request.user):
        messages.error(request, "Username or Password is incorrect!!!")
        return redirect('login')
    documents = Document.objects.filter(user=request.user)
    return render(request, 'home.html', {'documents': documents})


#signup
def SignuPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')
        else:
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists!")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return redirect('signup')
            else:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('login')

    return render(request, 'signup.html')


#login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!!!")

    return render(request, 'login.html')

#logout button
def LogoutPage(request):
    logout(request)
    request.session.clear()
    return redirect('login')


#upload
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            
            # Generate encryption key, IV, and salt
            encryption_key = get_random_bytes(16)  # AES-128
            iv = get_random_bytes(16)  # 128-bit IV for AES
            salt = base64.b64encode(get_random_bytes(8)).decode('utf-8')  # 8-byte salt, base64-encoded
            
            document.encryption_key = encryption_key
            document.iv = iv
            document.salt = salt
            
            # Read file content
            file_content = request.FILES['file'].read()
            
            # Compute file hash with salt
            document.file_hash = document.compute_hash(file_content)
            
            # Encrypt file content
            encrypted_file = document.encrypt_file(file_content)
            
            # Save encrypted file
            document.file.save(request.FILES['file'].name, ContentFile(encrypted_file))
            document.save()
            
            return redirect('home')
    else:
        form = DocumentForm()

    documents = Document.objects.filter(user=request.user)
    return render(request, 'home.html', {'documents': documents, 'form': form})


#download
@login_required
def document_download(request, document_id):
    # Get the document object based on the provided document_id
    document = get_object_or_404(Document, id=document_id)

    # Check if the current user is the owner of the document
    if document.user == request.user:
        fs = FileSystemStorage()
        encrypted_file_path = fs.path(document.file.name)  # Get the full path of the encrypted file

        try:
            # Read the encrypted file content from storage
            with open(encrypted_file_path, 'rb') as f:
                encrypted_file_data = f.read()
            
            # Decrypt the file content
            decrypted_data = document.decrypt_file(encrypted_file_data)
            # Compute the hash of the decrypted file content
            computed_hash = document.compute_hash(decrypted_data)
            
            # Verify if the computed hash matches the stored hash
            if computed_hash != document.file_hash:
                raise ValueError("File integrity check failed")
            
            # If integrity check passes, prepare the file for download
            response = HttpResponse(decrypted_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
            return response
        
        except ValueError as e:
            # Handle specific ValueErrors
            if str(e) == "Data must be padded to 16 byte boundary in CBC mode":
                # Error due to incorrect padding in the encryption process
                messages.error(request, "File corrupted cannot be downloaded!")
            else:
                # General ValueError, display the error message
                messages.error(request, str(e))
            return redirect('home')
        
        except Exception as e:
            # General exception handler for any other errors
            messages.error(request, "File corrupted cannot be downloaded!")
            return redirect('home')
    else:
        # If the user does not own the document, redirect to home
        return redirect('home')

#delete
@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.user == request.user:
        document.delete()
        messages.success(request, "Document deleted successfully.")
    return redirect('home')


#settings
@login_required
def settingsPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = request.user

        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username is already taken!')
        elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email is already in use!')
        elif password1 and password1 != password2:
            messages.error(request, 'Passwords do not match!')
        else:
            user.username = username
            user.email = email
            if password1:
                user.set_password(password1)
            user.save()
            messages.success(request, 'Your settings have been updated!')
            return render(request, 'settings.html')

    return render(request, 'settings.html')

#search
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet, SQ

@login_required
def search_view(request):
    query = request.GET.get('q')
    user = request.user  

    if query:
        # partial and full queries
        content_query = SQ(file__contains=query) & SQ(user_id=user.id)
        results = SearchQuerySet().filter(content_query).filter(user_id=user.id)
        results_data = [{'id': result.object.id, 'name': result.object.file.name} for result in results]
        
        # Debugging
        print("Search Query:", results.query)        
        # Debugging
        for result in results:
            print("File:", result.object.file.name)
            print("User ID:", result.object.user.id)
        
    else:
        results = []

    return JsonResponse({'results': results_data})




