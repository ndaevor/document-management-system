from django import forms
from .models import Document


#form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
