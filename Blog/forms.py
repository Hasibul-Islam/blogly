from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=255)
    
    image = forms.ImageField()
    image_credited = forms.CharField(max_length=255, required=False)
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'tags', 'category', 'image', 'image_credited', 'body']
