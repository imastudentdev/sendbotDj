from django import forms

class TelegramForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Ismingiz (ixtiyoriy)'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Xabaringiz...', 'rows': 5}), required=True)
    file = forms.FileField(required=False)
