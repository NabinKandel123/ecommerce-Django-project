from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from shop.models import Review
from django.forms import ModelForm

from shop.models import Contact



class ReviewForm(forms.ModelForm):
    def clean_rate(self):
        data = self.cleaned_data.get("rate", 5)
        if data < 0 or data > 5:
            raise forms.ValidationError("rate must be within range 1 to 5")
        return data

    class Meta:
        model = Review
        fields = ["rate", "review"]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]




class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

