from django.contrib import admin

from . models import Template, Link, Category, Image, Post

from django.utils.html import format_html
from django.urls import reverse


# Link zu ForeignKey
def linkify(field_name):
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  
    return _linkify

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', 'key')
    search_fields = ['name', 'key']
    readonly_fields = ["created_at", "updated_at"]

admin.site.register(Template, TemplateAdmin)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ['name', 'href']
    readonly_fields = ["created_at", "updated_at"]

admin.site.register(Link, LinkAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'linkName','order')
    list_filter = ('order', )
    search_fields = ['name']
    readonly_fields = ["created_at", "updated_at"]
admin.site.register(Category, CategoryAdmin)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', 'created_at')
    search_fields = ['title']
    readonly_fields = ["created_at", "updated_at"]
admin.site.register(Image, ImageAdmin)
class PostAdmin(admin.ModelAdmin):
    list_display = ("category","title",linkify(field_name="category"),linkify(field_name="template"))
    list_filter = ('title', "category", 'created_at')
    search_fields = ['title', 'category']
    list_display_links = ["category", ]

admin.site.register(Post, PostAdmin)








