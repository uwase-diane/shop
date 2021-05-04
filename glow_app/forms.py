from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Review


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    firstname = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'First name(optional)'
        }))
    lastname = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Last name'
        }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'1234 Main St'
        }))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Apartment, suite, etc.(optional)'
        }))
    city = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Kigali'
        }))
    country = CountryField(blank_label='(Choose..)').formfield(
        widget=CountrySelectWidget(attrs={
            'class':'custom-select d-block w-100'
        }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control'
           
        }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Phone'
        }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class SubscribeForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email Address')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['reviewer','review_title','review_body']
    
    