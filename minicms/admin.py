from .models import Config, Page
from django.contrib import admin

class PKChangingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # Delete entity with old pk if the pk has changed.
        # XXX: This doesn't update any references to the old entity, though.
        if change:
            pk = form.initial[self.model._meta.pk.attname]
            if obj.pk != pk:
                self.model.objects.filter(pk=pk).delete()

class PageAdmin(PKChangingAdmin):
    fields = ('url', 'title', 'content')
    list_display = ('url', 'title')
    search_fields = ('url',)

class ConfigAdmin(PKChangingAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Page, PageAdmin)
admin.site.register(Config, ConfigAdmin)
