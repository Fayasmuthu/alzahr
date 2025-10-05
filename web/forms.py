from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Your name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First name'}))
    last_name = forms.CharField(max_length=100, label='Your Last name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last name'}))
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '@email.com'}))
    phone = forms.CharField(label='Your phone', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter of your Number'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Please describe in detail your request'}))

