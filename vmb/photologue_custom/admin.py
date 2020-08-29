import os
import uuid

from django.contrib import admin

from photologue.admin import PhotoAdminForm, PhotoAdmin
from photologue.models import Photo


class PhotoCustomAdminForm(PhotoAdminForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["slug"].required = False


class PhotoCustomAdmin(PhotoAdmin):
    form = PhotoCustomAdminForm

    def save_model(self, request, obj, form, change):
        if not (obj.title and obj.slug):
            obj.title = obj.slug = uuid.uuid5(uuid.uuid1(), str(os.getpid())).hex[:32]
        super().save_model(request, obj, form, change)


admin.site.unregister(Photo)
admin.site.register(Photo, PhotoCustomAdmin)
