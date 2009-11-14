import views
import userforms as forms
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template import RequestContext
from django.contrib.sites.models import Site, RequestSite
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def user_creation (request, template_name='registration/create_user.html'):
    if request.method == 'POST':
       user_creation_form = forms.UserCreationForm(request.POST)
       if user_creation_form.is_valid():
          username = user_creation_form.cleaned_data['username']
          password = user_creation_form.cleaned_data['password1']
          User.objects.create_user(username, '', password)
          return HttpResponseRedirect('/accounts/login/')
    elif request.method == 'GET':
       user_creation_form = forms.UserCreationForm()
    return render_to_response(template_name, {'form':user_creation_form}, context_instance=RequestContext(request))

def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """Displays the login form and handles the login action."""
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    if request.method == 'POST':
       login_form = forms.AuthenticationForm(request.POST)
       login_form.set_request(request)
       if login_form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                from django.conf import settings
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            user = login_form.user
            login(request, user)
            request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    elif request.method == 'GET':
        login_form = forms.AuthenticationForm()
    request.session.set_test_cookie()
    return render_to_response(template_name, {
        'form': login_form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def logout(request, next_page=None, template_name='registration/logged_out.html'):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)
    if next_page is None:
        return render_to_response(template_name, {'title': _('Logged out')}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def logout_then_login(request, login_url=None):
    "Logs out the user if he is logged in. Then redirects to the log-in page."
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL
    return logout(request, login_url)

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    "Redirects the user to the login page, passing the given 'next' page"
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL
    return HttpResponseRedirect('%s?%s=%s' % (login_url, redirect_field_name, next))

def password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html'):
    if request.method == 'POST':
       form = forms.PasswordResetForm(request.POST)
       if form.is_valid():
            if is_admin_site:
                form.save(domain_override=request.META['HTTP_HOST'])
            else:
                form.save(email_template_name=email_template_name)
            return HttpResponseRedirect('%sdone/' % request.path)       
    elif request.method == 'GET':
        form = forms.PasswordResetForm()
    print template_name
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

def index(request):
    return render_to_response('registration/password_reset_form.html', {}, context_instance=RequestContext(request))

def password_change(request, template_name='registration/password_change_form.html'):
    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST)
        form.set_user(request.user)
        if form.is_valid():
            form.save(form.cleaned_data['new_password1'])
            return HttpResponseRedirect('%sdone/' % request.path)       
    if request.method == 'GET':
        form = forms.PasswordChangeForm()
    return render_to_response(template_name, {'form': form},
        context_instance=RequestContext(request))
password_change = login_required(password_change)

def user_change_password(request, id):
    if not request.user.has_perm('auth.change_user'):
        raise PermissionDenied    
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = forms.AdminPasswordChangeForm(request.POST)
        form.set_user(user)
        if form.is_valid():
            new_user = form.save()
            msg = _('Password changed successfully.')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect('..')
    elif request.method == 'GET':
        form = forms.AdminPasswordChangeForm()
    return render_to_response('admin/auth/user/change_password.html', {'title': _('Change password: %s') % user.username, 'form': form, 'is_popup': '_popup' in request.REQUEST, 'add': True, 'change': False, 'has_delete_permission': False, 'has_change_permission': True, 'has_absolute_url': False, 'opts': User._meta, 'original': user, 'show_save': True, }, context_instance=RequestContext(request))

@login_required
def profile (request):
    return views.user_account(request, request.user.username)