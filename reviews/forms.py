from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(i, f'{i} - {"Star" if i == 1 else "Stars"}') for i in range(1, 6)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Review
        fields = [
            'rating',
            'comment',
        ]

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this stay...',
            }),
        }

        labels = {
            'rating': 'Rating',
            'comment': 'Your Review',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                'Rating must be between 1 and 5.'
            )

        return rating
