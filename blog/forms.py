from django import forms
from .models import Blog, Tag

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'context', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'context': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your blog content here...', 'rows': 6}),
        }
