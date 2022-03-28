from django.contrib import admin
from .models import *


class ForumListAdmin(admin.ModelAdmin):
    fields = ('title', 'text')

admin.site.register(ForumList, ForumListAdmin)



