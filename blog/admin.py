from django.contrib import admin
import models

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("titulo",)}
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(models.Category)
admin.site.register(models.Post, PostAdmin)
