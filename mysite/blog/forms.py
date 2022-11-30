from django import forms


class EmailPostForm(forms.Form):
    from_name = forms.CharField(max_length=25)
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    share_message = forms.CharField(required=False, widget=forms.Textarea)
