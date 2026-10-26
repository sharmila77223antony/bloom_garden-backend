
from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "description",
            "image",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "glass-input",
                "placeholder": "Give your story a title",
            }),
            "description": forms.Textarea(attrs={
                "class": "glass-input",
                "placeholder": "Write your story here...",
                "rows": 6,
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "glass-input",
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "glass-checkbox",
            }),
        }
