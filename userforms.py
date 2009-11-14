from django import forms
import re
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext as _

class UserCreationForm(forms.Form):
    """A form that creates a user, with no privileges, from the given username and password."""
    username = forms.CharField(max_length = 30, required = True)
    password1 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    password2 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)

    def clean_username (self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['username']):
            raise ValidationError("This value must contain only letters, numbers and underscores.")
        self.isValidUsername()
        return self.cleaned_data['username']

    def clean (self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_("The two password fields didn't match."))
        return super(forms.Form, self).clean()
        
    def isValidUsername(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return
        raise ValidationError(_('A user with that username already exists.'))

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(required = True, max_length = 30)
    password = forms.CharField(required = True, max_length = 30, widget = forms.PasswordInput)
    def set_request (self, request):
        self.request = request
        
        
    def clean (self):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
	if self.request and not self.request.session.test_cookie_worked():
	    raise ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))
        if user is None:
            raise ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
        elif not user.is_active:
            raise ValidationError(_("This account is inactive."))
        else:
            self.user = user
        return super(forms.Form, self).clean()

class PasswordResetForm(forms.Form):
    """A form that lets a user request a password reset"""
    email = forms.EmailField(required = True)

    def clean_email (self):
        try:
           self.user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            print '***'
            raise ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return self.cleaned_data['email']

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html'):
        "Calculates a new password randomly and sends it to the user"
        from django.core.mail import send_mail
        user = self.user
        new_pass = User.objects.make_random_password()
        user.set_password(new_pass)
        user.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
        'new_password': new_pass,
        'email': user.email,
        'domain': domain,
        'site_name': site_name,
        'user': user,
        }
        send_mail(_('Password reset on %s') % site_name, t.render(Context(c)), None, [user.email])

class PasswordChangeForm(forms.Form):
    """A form that lets a user change his password."""
    old_password = forms.CharField(widget=forms.PasswordInput, required = True, max_length = 30)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required = True, max_length = 30)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required = True, max_length = 30)

    def set_user (self, user):
        self.user = user

    def clean_old_password (self):
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return self.cleaned_data['old_password']

    def clean (self):
         if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
             raise ValidationError(_("The two new password fields didn't match."))
         return super(forms.Form, self).clean()

    def save (self, new_password):
        "Saves the new password."
        self.user.set_password(new_password)
        self.user.save()

class AdminPasswordChangeForm(forms.Form):
    """A form used to change the password of a user in the admin interface."""
    password1 = forms.CharField(widget = forms.PasswordInput, max_length = 30, required = True)
    password2 = forms.CharField(widget = forms.PasswordInput, max_length = 30, required = True)	
    
    def set_user (self, user):
        self.user = user
    	
    def clean (self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_("The two password fields didn't match."))
        return super(forms.Form, self).clean()

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()      
      