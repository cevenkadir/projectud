from django import forms

class UploadParticlesForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}
        )
        )