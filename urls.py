from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^djikiki/', include('djikiki.urls')),
    (r'^accounts/', include('registration.urls')),

)

urlpatterns += patterns('',
     ('^admin/(.*)', admin.site.root),
    )

if settings.DEBUG:
    import os
    dirname = os.path.dirname(globals()["__file__"])
    media_dir = os.path.join(dirname, 'site_media')
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_dir}),
        
        )

