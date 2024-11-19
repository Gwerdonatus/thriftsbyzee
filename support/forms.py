from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer_name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
