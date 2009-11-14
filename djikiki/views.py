from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import random

import forms
import djikikisettings
from decorators import handle404, check_wiki_installed
from models import *


@check_wiki_installed
def index (request):
    featured_pages = FeaturedPage.objects.all().order_by('-ordering')
    try:
       latest_featured = featured_pages[0].page
    except IndexError:
       latest_featured = ''
    recently_featured = featured_pages[:djikikisettings.recently_featured]
    payload = {'latest_featured':latest_featured, 'recently_featured':recently_featured}
    return render(request, 'djikiki/index.html', payload)

@check_wiki_installed
@handle404
def detail (request, slug, mode = 'article'):
    page = Page.objects.get(slug = slug)
    categories = [category for category in page.current_revision.categories.all()]
    if mode == 'article':
        payload = {'page':page, 'categories':categories,}
        return render(request, 'djikiki/detail.html', payload)
    elif mode == 'discuss':    
        payload = {'page':page, 'categories':categories, }
        return render(request, 'djikiki/discuss.html', payload)

@check_wiki_installed
@handle404
def category (request, text):
    try:
       page_num = request.GET['page']
       page_num = int(page_num)
    except:
       page_num = 1    
    category = Category.objects.get(text = text)
    page_revs = category.pagerevision_set.all()
    pages = Page.objects.filter(current_revision__in = page_revs)
    pages_ = Paginator(pages, djikikisettings.details_per_page)
    next_page = page_num + 1
    prev_page = page_num - 1
    pages = pages_.page(page_num)
    has_next = pages.has_next()
    has_previous = pages.has_previous()    
    payload = {'category':category, 'pages':pages.object_list,  'has_next':has_next, 'has_previous':has_previous, 'next_page':next_page, 'prev_page':prev_page }
    return render(request, 'djikiki/category.html', payload)

@check_wiki_installed
@handle404
def revisions (request, slug, mode='article'):
    page = Page.objects.get(slug = slug)
    if mode == 'article':
        is_discussion = False
        page_revisions = PageRevision.objects.filter(revision_for = page, is_discussion = is_discussion).order_by('-revision_num')
    else:
        is_discussion = True
        page_revisions = PageRevision.objects.filter(revision_for = page, is_discussion = is_discussion).order_by('-revision_num')
    try:
       page_num = request.GET['page']
       page_num = int(page_num)
    except:
       page_num = 1
    page_revisions_ = Paginator(page_revisions, djikikisettings.details_per_page)
    next_page = page_num + 1
    prev_page = page_num - 1
    page_revisions = page_revisions_.page(page_num)
    has_next = page_revisions.has_next()
    has_previous = page_revisions.has_previous()    
    payload = {'page':page, 'revisions':page_revisions.object_list, 'has_next':has_next, 'has_previous':has_previous, 'next_page':next_page, 'prev_page':prev_page }
    return render(request, 'djikiki/revisions.html', payload)   

@check_wiki_installed
@handle404
def old_page (request, id):
    page_revision = PageRevision.objects.get(id = id)
    categories = [category for category in page_revision.categories.all()]
    payload = {'page_revision':page_revision, 'categories':categories}
    return render(request, 'djikiki/oldpage.html', payload)

def random_page (request):
    page_count = Page.objects.all().count()
    random_page_id = random.randint(1, page_count)
    page = Page.objects.get(id = random_page_id)
    title = '/page/%s/' % page.slug
    return HttpResponseRedirect(title)

def recently_featured (request):
    import pdb
    #pdb.set_trace()
    featured = FeaturedPage.objects.all().order_by('-ordering')
    paged_featured = Paginator(featured, djikikisettings.details_per_page)
    try:
       page_num = request.GET['page']
       page_num = int(page_num)
    except:
       page_num = 1
    next_page = page_num + 1
    prev_page = page_num - 1
    featured = paged_featured.page(page_num)
    has_next = featured.has_next()
    has_previous = featured.has_previous()
    payload = {'featured':featured.object_list, 'has_next':has_next, 'has_previous':has_previous, 'next_page':next_page, 'prev_page':prev_page}
    return render(request, 'djikiki/featured.html', payload)    

@check_wiki_installed
@login_required    
def create (request):
    if request.method == 'POST':
        create_form = forms.CreatePage(request.POST)
        if create_form.is_valid():
            page = create_form.save(request.user)
            return HttpResponseRedirect(page.get_absolute_url())
    if request.method == 'GET':
        create_form = forms.CreatePage()
    payload = {'form':create_form}
    return render(request, 'djikiki/create.html', payload)      

@check_wiki_installed
@login_required
@handle404
def edit (request, slug, mode = 'article'):
    if request.method == 'POST':
        page = None
        edit_form = forms.EditPage(page, request.POST)
        if edit_form.is_valid():
            page = edit_form.save(slug, request.user)
            return HttpResponseRedirect(page.get_absolute_url())                
    if request.method == 'GET':
        page = Page.objects.get(slug = slug)
        edit_form = forms.EditPage(page)
    payload = {'form':edit_form, 'page':page}
    return render(request, 'djikiki/edit.html', payload)

@check_wiki_installed
@login_required
@handle404
def discuss_edit (request, slug):
    if request.method == 'POST':
        page = None
        edit_form = forms.DiscussEditPage(page, request.POST)
        if edit_form.is_valid():
            page = edit_form.discuss_save(slug, request.user)
            return HttpResponseRedirect(page.get_discuss_url())         
    if request.method == 'GET':
        page = Page.objects.get(slug = slug)
        edit_form = forms.DiscussEditPage(page)
    payload = {'form':edit_form, 'page':page}
    return render(request, 'djikiki/edit.html', payload)

@check_wiki_installed
@handle404
def user_account (request, username):
    user_for = User.objects.get(username = username)
    user_edits = PageRevision.objects.filter(user = user_for)
    user_create = Page.objects.filter(user = user_for)
    payload = {'user_edits':user_edits, 'user_create':user_create,'user_for':user_for}
    return render(request, 'djikiki/useredits.html', payload)   

def render (request, template, payload):
    recent_pages = Page.objects.all().order_by('-created_on')[:5]
    recent_changes = Page.objects.all().order_by('-modified_on')[:5]
    try:
        wiki = Wiki.objects.latest()
    except:
        wiki = ''
    payload.update({'wiki':wiki})
    payload.update({'recent_pages':recent_pages, 'recent_changes':recent_changes})
    return render_to_response(template, payload, RequestContext(request))

def administer (request):
    """Provides administaration functions"""
    pass
        

     