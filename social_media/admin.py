from django.contrib import admin

from social_media.models import User, Post, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)