from django import forms


class URLForm(forms.Form):
    user_url = forms.URLField(label='Your URL', max_length=100)
    user_hash = forms.CharField(label='Your hash', max_length=15, required=False)
