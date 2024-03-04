from django import forms
from .models import Client, Lawyer

class ClientSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Client
        fields = ['name', 'profile_picture', 'location','phone', 'email', 'password','confirm_password']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")

class LawyerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Lawyer
        fields = ['name', 'profile_picture', 'location', 'email', 'password','confirm_password', 'specialization_tags', 'profile_description']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")

# class AcademicStatusForm(forms.ModelForm):
#     class Meta:
#         model = Academic
#         fields = ['academic_degree', 'completion_year', 'major_subject']

# # class LicenseDetailsForm(forms.ModelForm):
#     class Meta:
#         model = License
#         fields = ['license_no', 'license_location']