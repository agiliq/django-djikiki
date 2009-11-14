from django.contrib import admin
from djikiki.models import Wiki, Category, PageRevision, Page, FeaturedPage


admin.site.register(Wiki)
admin.site.register(Category)
admin.site.register(PageRevision)
admin.site.register(Page)
admin.site.register(FeaturedPage)