from django import forms
import models
from datetime import datetime

class WideTextArea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{}).update({'rows': '20', 'cols':'80'})
        super(WideTextArea, self).__init__(*args, **kwargs)

class CreatePage(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget = WideTextArea)
    edit_summary = forms.CharField()
    categories = forms.CharField(required = False)

    def save(self, user):
        page = models.Page(title = self.cleaned_data['title'], user = user)
        page.save()
        page_revision = models.PageRevision(wiki_text = self.cleaned_data['text'], edit_summary = self.cleaned_data['edit_summary'], user = user, revision_for = page)
        page_revision.save()
        discuss_revision = models.PageRevision(wiki_text = 'Auto created first revision.', edit_summary = '', user = user, revision_for = page, is_discussion = True)
        discuss_revision.save()
        categories_list = self.cleaned_data['categories'].split()
        for category in categories_list:
            try:
                cat_ = models.Category.objects.get(text = category)
            except models.Category.DoesNotExist:
                cat_ = models.Category(text = category)
                cat_.save()
            page_revision.categories.add(cat_)
        page.current_revision = page_revision
        page.current_disc_rev = discuss_revision
        page.save()
        return page
    

class EditPage(forms.Form):
    text = forms.CharField(widget = WideTextArea)
    edit_summary = forms.CharField()
    categories = forms.CharField(required = False)
    
    def __init__(self, page_ = None, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        if not page_ is None:
            self.fields['text'].initial = page_.current_revision.wiki_text
            categories = ''
            for category in page_.current_revision.categories.all():
                categories += category.text
                categories += ' '        
            self.fields['categories'].initial = categories

    def save (self, slug, user):
        page = models.Page.objects.get(slug = slug)
        revision_count = models.PageRevision.objects.filter(revision_for = page, is_discussion = False).count()
        new_rev = revision_count + 1
        page_revision = models.PageRevision(wiki_text = self.cleaned_data['text'], edit_summary = self.cleaned_data['edit_summary'], user = user, revision_for = page, revision_num = new_rev)
        page_revision.save()
        categories_list = self.cleaned_data['categories'].split()
        for category in categories_list:
            try:
                cat_ = models.Category.objects.get(text = category)
            except models.Category.DoesNotExist:
                cat_ = models.Category(text = category)
                cat_.save()
            page_revision.categories.add(cat_)
        page.current_revision = page_revision
        page.modified_on = datetime.now()
        page.save()
        return page

class DiscussEditPage(forms.Form):
    text = forms.CharField(widget = WideTextArea)
    edit_summary = forms.CharField()

    def __init__(self, page_ = None, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        if not page_ is None:
            self.fields['text'].initial = page_.current_disc_rev.wiki_text
            
    def discuss_save (self, slug, user):
        page = models.Page.objects.get(slug = slug)
        revision_count = models.PageRevision.objects.filter(revision_for = page, is_discussion = True).count()
        new_rev = revision_count + 1
        page_revision = models.PageRevision(wiki_text = self.cleaned_data['text'], edit_summary = self.cleaned_data['edit_summary'], user = user, is_discussion = True, revision_for = page, revision_num = new_rev)
        page_revision.save()
        page.current_disc_rev = page_revision
        page.modified_on = datetime.now()
        page.save()
        return page

class MakeFeatured(forms.Form):
    title = forms.CharField()
    def save (self):
        page = models.Page.objects.get(title = self.cleaned_data['title'])
        fpage = models.FeaturedPage(page = page)
        fpage.save()

class InstallForm (forms.Form):
    """Installation data. Just the name of the wiki, really"""
    name = forms.CharField()
    tagline = forms.CharField()
    def save (self):
        wiki = models.Wiki(name = self.cleaned_data['name'], tagline = self.cleaned_data['tagline'])
        wiki.save()
        
        



        
        

        
        

        