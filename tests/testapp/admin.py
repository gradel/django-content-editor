from django import forms
from django.contrib import admin
from django.db import models

from content_editor.admin import ContentEditor, ContentEditorInline

from .models import Article, Download, RichText, Thing


class RichTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {"class": "richtext"}
        if attrs:  # pragma: no cover
            default_attrs.update(attrs)
        super(RichTextarea, self).__init__(default_attrs)


class RichTextInline(ContentEditorInline):
    model = RichText
    formfield_overrides = {models.TextField: {"widget": RichTextarea}}
    fieldsets = [(None, {"fields": ("text", "region", "ordering")})]
    regions = ("main",)

    class Media:
        js = ("//cdn.ckeditor.com/4.5.6/standard/ckeditor.js", "app/plugin_ckeditor.js")


class ThingInline(admin.TabularInline):
    model = Thing


admin.site.register(
    Article,
    ContentEditor,
    inlines=[
        RichTextInline,
        ContentEditorInline.create(
            model=Download, regions=lambda inline, regions: regions - {"sidebar"}
        ),
        ThingInline,
    ],
)
