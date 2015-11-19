from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from main.models import GroupProfile, UserProfile
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60)
    body = RichTextField()
    poster = models.ForeignKey(User, null=True)
    group = models.ForeignKey(GroupProfile, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def commentCount(self):
        return Comment.objects.filter(post=self).count()
    def __unicode__(self):
        return self.title
    def author(self):
        return self.poster

### Admin
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, null=True)
    group = models.ForeignKey(GroupProfile, null=True)
    body = RichTextField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
    def poster_picture(self):
	userprofile = UserProfile.objects.get(user=self.poster)
	return userprofile.picture_path()

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
