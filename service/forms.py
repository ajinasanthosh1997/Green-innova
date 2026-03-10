from django import forms
from .models import AcademyEnrollment

class AcademyEnquiryForm(forms.ModelForm):

    class Meta:
        model = AcademyEnrollment
        fields = ["full_name", "email", "phone", "course", "background"]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
            "course": forms.Select(attrs={"class": "input"}),
            "background": forms.Textarea(attrs={"class": "input"}),
        }
