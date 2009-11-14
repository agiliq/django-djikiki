from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from models import Wiki

def handle404 (view_function):
    """If we are not in debug mode, convert ObjectDoesNotExist to Http404"""
    def wrapper (*args, **kwargs):
        if not settings.DEBUG:
            try:
                return view_function (*args, **kwargs)
            except ObjectDoesNotExist:
                raise Http404
        else:
            return view_function (*args, **kwargs)
    return wrapper

def check_wiki_installed(view_function):
    def is_install(*args, **kwargs):
        if Wiki.objects.all().count():
            return view_function(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('djikiki_install'))
    return is_install