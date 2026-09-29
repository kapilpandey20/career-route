from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']

        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")

        return file