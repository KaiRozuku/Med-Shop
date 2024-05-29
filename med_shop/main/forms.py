from django import forms
from .models import Profile


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'profile_picture': 'Upload Profile Picture',
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')

        if picture:
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("The profile picture size must be under 5MB.")
            if not picture.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("The profile picture must be in JPEG or PNG format.")

        return picture