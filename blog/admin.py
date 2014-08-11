from django.contrib import admin
import models

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("titulo",)}

admin.site.register(models.Post, PostAdmin)
