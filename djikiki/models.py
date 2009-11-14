from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import permalink
from django.core.urlresolvers import reverse

import random
from creole import creole, creole2html

class Wiki(models.Model):
    """Stores site wide preferences"""
    name = models.TextField(max_length = 30)
    tagline = models.TextField(max_length = 100)

    def save (self):
        if Wiki.objects.all().count() and not self.id:
           raise Exception('Only one Wiki object allowed')
        super(Wiki, self).save()

    def __str__ (self):
        return self.name        
    
    class Meta:
        get_latest_by = 'id'

class Category(models.Model):
    """Category under which a page is classified. ManyToMany relationship with pages."""
    text = models.SlugField(max_length = 100, unique = True)

    def __str__ (self):
        return 'Category: %s' % self.text
    
    @models.permalink
    def get_absolute_url (self):
        return ('djikiki.views.category', [self.text])

class PageRevision(models.Model):
    """Stores a specific revision of the page"""
    wiki_text = models.TextField()
    html_text = models.TextField()
    edit_summary = models.TextField(max_length = 100)
    user = models.ForeignKey(User)
    is_discussion = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add = 1)
    categories = models.ManyToManyField(Category)
    revision_for = models.ForeignKey('Page')
    revision_num = models.IntegerField(default = 0)
    
    def save (self): 
        document = creole.Parser(self.wiki_text).parse()
        self.html_text = creole2html.HtmlEmitter(document).emit()
        #self.html_text = creoleparser.creole2html(self.wiki_text)
        super(PageRevision, self).save() # Call the "real" save() method.

    def __str__ (self):
        return '%s-%s' % (self.edit_summary, self.wiki_text)
    
    @models.permalink
    def get_absolute_url (self):
        return ('djikiki.views.old_page', [self.id])

class Page(models.Model):
    """Stores the latest page, the page which needs to be displayed to the user."""
    title = models.SlugField(unique = True, max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True)
    created_on = models.DateTimeField(auto_now_add = 1)
    modified_on = models.DateTimeField(auto_now_add = 1)
    current_revision = models.ForeignKey(PageRevision, related_name = 'main', blank = True, null = True)        
    current_disc_rev =  models.ForeignKey(PageRevision, related_name = 'discussion', blank = True, null = True) 
    user = models.ForeignKey(User)
    
    def save (self):
        if not self.slug:               
                self.slug = '-'.join(self.title.split())
                try:
                    Page.objects.get(slug = self.slug)
                except ObjectDoesNotExist, e:
                    pass
                else:
                   count = Page.objects.filter(slug__contains = self.slug).count()
                   self.slug = '%s-%s' % (self.slug, str(count + 1))
                   self.title = '%s-%s' % (self.title, str(count + 1))
        super(Page, self).save() # Call the "real" save() method    
    
    
    @models.permalink
    def get_absolute_url (self):
        return ('djikiki.views.detail', [self.slug])
    
    def get_discuss_url (self):
        return reverse('djikiki_discuss', args=[self.slug])
        
    @models.permalink
    def get_edit_url (self):
        return ('djikiki.views.edit', [self.slug])

    def get_discuss_edit_url (self):
        return reverse('djikiki_discuss_edit', args=[self.slug])
    
    @models.permalink
    def get_revision_url (self):
        return ('djikiki.views.revisions', [self.slug])

    def get_discuss_revision_url (self):
        return reverse('djikiki_discuss_revisions', args=[self.slug])

    def __str__ (self):
        return self.title

class FeaturedPage(models.Model):
    featured_on = models.DateField(auto_now_add = 1)
    page = models.ForeignKey(Page, unique = True)
    ordering = models.IntegerField(default = 0, unique = True)

    def save (self):
        count = FeaturedPage.objects.all().count()
        if count > 0:
            self.ordering = count + 1
        super(FeaturedPage, self).save()
        

    def __str__ (self):
        return '%s - %s' % (self.featured_on, self.page.title)

    class Meta:
        get_latest_by = '-ordering'
        