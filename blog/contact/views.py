from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags

## Function for sending an enquiry
def post_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            recipients = [settings.EMAIL_HOST_USER] # Called from settings.py to define the recipients
            context = {
                "name": name,
                "message": message,
                "email": email,
                "subject": subject
            } # Data to be passed to mail_content.html is stored in context.
            html_content = render_to_string("mail/basic/index.html", context) # Read and store the code of mail_contact.html in html_content.
            text_content = strip_tags(html_content) # Reads as text data by omitting tags from the imported html.
            try:
                send_mail(subject=subject, message=text_content, from_email=email, recipient_list=recipients,  html_message=html_content)
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            messages.add_message(request, messages.SUCCESS, _("Your enquiry has been sent to LandLim")) # Throw a message to the HTML side.
            return render(request, 'contact/post_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})