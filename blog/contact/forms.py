from django import forms

## Form classes for contacting us
class ContactForm(forms.Form):
   name = forms.CharField(label='お名前', max_length=50)
   email = forms.EmailField(label='メールアドレス',)
   message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea)
   subject = forms.CharField(label='件名', required=False)

## A form class for storing the user's email address.
class SaveEmail(forms.Form):
    email = forms.EmailField(label='メールアドレス')