from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^djikiki/', include('djikiki.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# if settings.DEBUG:
#     import os
#     dirname = os.path.dirname(globals()["__file__"])
#     media_dir = os.path.join(dirname, 'site_media')
#     urlpatterns += patterns('',
#         (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_dir}),
        
#         )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)