from actstream.admin import ActionAdmin 
from django.contrib import admin

from actstream import models

# Use django-generic-admin widgets if available
try:
    from genericadmin.admin import GenericAdminModelAdmin as ModelAdmin
except ImportError:
    ModelAdmin = admin.ModelAdmin


from vmb.users.models import User

class MyCustomListFilter(admin.SimpleListFilter):
   title = 'By User'
   parameter_name = 'user'

   def lookups(self, request, model_admin):
        users = User.objects.all()
        choices = []
        for user in users:
            choices.append((
                f'{str(user)}',f'{str(user)}'
            ))
        choices = tuple(choices)
        print("lookups:",choices)
        return choices

   def queryset(self, request, queryset):
        print("queryset:",self.value())
        if self.value() is not None:
            user = User.objects.get(username=self.value())
            return queryset.filter(actor_object_id=user.id)
        else:
            return queryset

class CustomActionAdmin(ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__str__', 'actor', 'verb', 'target', 'public')
    list_editable = ('verb',)
    list_filter = ('timestamp', MyCustomListFilter)

admin.site.unregister(models.Action)
admin.site.register(models.Action, CustomActionAdmin)
