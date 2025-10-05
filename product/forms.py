from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["fullname", "content", "rating"]
        widgets = {
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Full Name"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
             'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)],attrs={'class':"form-select", 'required id':"review-rating"}),
        }



