from django.contrib import admin
from .models import Plugin, Dependency, Introduction, Description, Download

# Register your models here.
admin.site.register(Plugin)
admin.site.register(Dependency)
admin.site.register(Introduction)
admin.site.register(Description)
admin.site.register(Download)