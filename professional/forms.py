from django import forms
from .models import ProReview


class ProReviewForm(forms.ModelForm):

    class Meta:
        model = ProReview
        fields = ['title', 'rank', 'content']