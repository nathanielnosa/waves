from django import forms
from . models import Customer
class CustomerProfile(forms.ModelForm):
    password1 = forms.CharField(label=('Password'),widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=('Confirm Password'),widget=forms.PasswordInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Customer
        fields = ['fullname','email','username','password1','password2','phone']
        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
        }