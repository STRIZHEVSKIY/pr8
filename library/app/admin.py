from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, City, PDFFile

admin.site.register(User)
admin.site.register(City)
admin.site.register(PDFFile)
admin.site.unregister(Group)
