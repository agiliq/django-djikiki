from django.conf.urls.defaults import *
urlpatterns = patterns('djikiki.views',
    url(r'^$', 'index', name='djikiki_index'),
    url(r'^create/$', 'create', name='djikiki_create'),
    url(r'^page/(?P<slug>[^\.^/]+)/$', 'detail', name='djikiki_detail'),
    url(r'^edit/(?P<slug>[^\.^/]+)/$', 'edit', name='djikiki_edit'),
    url(r'^page/(?P<slug>[^\.^/]+)/revisions/$', 'revisions', name='djikiki_revisions'),
    url(r'^discuss/(?P<slug>[^\.^/]+)/$', 'detail', {'mode':'discuss'}, name='djikiki_discuss'),
    url(r'^discuss-edit/(?P<slug>[^\.^/]+)/$', 'discuss_edit', name='djikiki_discuss_edit'),
    url(r'^discuss/(?P<slug>[^\.^/]+)/revisions/$', 'revisions', {'mode':'discuss'}, name='djikiki_discuss_revisions'),
    url(r'^category/(?P<text>[^\.^/]+)/$', 'category', name='djikiki_category'),
    url(r'^revision/(?P<id>\d+)/$', 'old_page', name='djikiki_old_page'),
    url(r'^user-edit/(?P<username>\w+)/$', 'user_account', {}, name='djikiki_useredits'),
    url(r'^random/$', 'random_page', {}, name='djikiki_random'),
    url(r'^featured/$', 'recently_featured', {}, name='djikiki_featured'),

    )

urlpatterns += patterns('djikiki.adminviews',
    url(r'^administration/create-featured/$', 'create_featured', {}, name='djikiki_create_featured'),
    url(r'^administration/user-list/$', 'user_list', {}, name='djikiki_userlist'),
    url(r'^administration/install/$', 'install', {}, name='djikiki_install'),
   )

urlpatterns += patterns('djikiki.userviews',
    url(r'^profile/$', 'profile', name= 'djikiki_profile'),
   )


