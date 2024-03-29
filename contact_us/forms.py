from django import forms
from django.core import mail


class ContactUsForm(forms.Form):
    attrs = {"class": "form-control", 'required': 'required'}
    name = forms.CharField(max_length=50, label='Name', widget=forms.TextInput(attrs=attrs))
    email = forms.EmailField(max_length=30, label='Email', widget=forms.TextInput(attrs=attrs))
    msg = forms.CharField(max_length=500, label='Message', widget=forms.Textarea(attrs=attrs))

    def send_contactus_mail(self):
        success = False
        name = self.cleaned_data['name']
        subject = "{0} from My Study Notebook wants to contact you".format(name)
        msg = self.cleaned_data['msg']
        from_email = self.cleaned_data['email']
        to_email = ('tareqbuet@gmail.com',)  # must be a list or tuple
        try:
            mail.send_mail(subject, msg, from_email, to_email, fail_silently=False)
        except Exception as ex:
            print(type(ex).__name__, ex.args)
        else:
            success = True
        return success
