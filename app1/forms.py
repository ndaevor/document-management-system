from django import forms
from .models import Document
from django.core.exceptions import ValidationError

# List of allowed file extensions
ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx']

def validate_file_extension(value):
    if not any(value.name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValidationError('Unsupported file extension.')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
    file = forms.FileField(validators=[validate_file_extension])


