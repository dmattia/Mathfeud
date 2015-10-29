from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    author = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)

    def commentCount(self):
        return Comment.objects.filter(post=self).count()

    def __unicode__(self):
        return self.title
### Admin
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

