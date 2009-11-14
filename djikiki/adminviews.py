import forms
from views import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decorators import handle404, check_wiki_installed

@check_wiki_installed
@login_required
def create_featured (request):
    if not request.user.is_staff:
        return HttpResponseForbidden()    
    if request.method == 'POST':
        featured_page_form = forms.MakeFeatured(request.POST)
        if featured_page_form.is_valid():
            featured_page_form.save()
            return HttpResponseRedirect('.')    
    elif request.method == 'GET':
        featured_page_form = forms.MakeFeatured()
    payload = {'form':featured_page_form}
    return render(request, 'djikiki/edit.html', payload)
        
@check_wiki_installed        
@login_required
def user_list (request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    user_list = User.objects.all()
    payload = {'user_list':user_list}
    return render(request, 'djikiki/userlist.html', payload)

@login_required
def install (request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST' :
        install_form = forms.InstallForm(request.POST)
        if install_form.is_valid():
            install_form.save()
            return HttpResponseRedirect('/')
    elif request.method == 'GET':
        install_form = forms.InstallForm()
    payload = {'form':install_form}
    return render(request, 'djikiki/edit.html', payload)        
        
    
        
    