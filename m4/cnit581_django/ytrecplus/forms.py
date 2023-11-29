from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=32)
    password = forms.CharField(label="Password", max_length=32)
    
class LogoutForm(forms.Form):
    logout = forms.CharField(label="Logout Action", widget = forms.HiddenInput())
    
class ProfileSwitchForm(forms.Form):
    profile = forms.CharField(label="Profile Name", widget = forms.HiddenInput())
    
class UploadForm(forms.Form):
    CATEGORIES = [
        ('science', 'Science'),
        ('nature', 'Nature'),
    ]
    title = forms.CharField(label="Video Title", max_length=64)
    description = forms.CharField(widget=forms.Textarea(), label="Description", max_length=1024)
    category = forms.ChoiceField(label="Category", widget=forms.RadioSelect, choices=CATEGORIES)
    channel = forms.CharField(label="Channel", max_length=64)
  
class CommentForm(forms.Form):
    video = forms.IntegerField()
    name = forms.CharField(max_length=64, help_text="Enter user identifier", widget = forms.HiddenInput())
    text = forms.CharField(max_length=500, help_text="Enter a brief comment for the video")