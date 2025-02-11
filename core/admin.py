from django.contrib import admin
from .models import ForumPost, UserMessage

admin.site.register(ForumPost)
admin.site.register(UserMessage) 