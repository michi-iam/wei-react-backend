from django.db import models
from datetime import datetime

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Template(TimeStampedModel):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.key

class Link(TimeStampedModel):
    name = models.CharField(max_length=60)
    href = models.CharField(max_length=150)
    def __str__(self):
        return self.name
       
class Category(TimeStampedModel):
    name = models.CharField(max_length=50)
    linkName = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return self.name

class Image(TimeStampedModel):
    title = models.CharField(max_length=75, blank=True, null=True)
    src = models.CharField(max_length=200)
    alt = models.TextField()
    slideTitle = models.CharField(max_length=75, blank=True, null=True)
    slideText = models.CharField(max_length=150, blank=True, null=True)
    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id) 


class Post(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="post_category", blank=True)#
    template = models.ForeignKey(Template, on_delete=models.PROTECT, related_name="post_template", blank=True)#
    links = models.ManyToManyField(Link, related_name="post_links", null=True, blank=True)#
    mainImage = models.ForeignKey(Image, on_delete=models.PROTECT, related_name="post_mainimage", null=True, blank=True)#
    images = models.ManyToManyField(Image, related_name="post_images", null=True, blank=True)#
    order = models.PositiveIntegerField(default=1, blank=True)
    active = models.BooleanField(default=False, blank=True)#
    linkName = models.CharField(max_length=60, blank=True)#
    title = models.CharField(max_length=100)#
    subTitle = models.CharField(max_length=200, blank=True, null=True)#
    text = models.TextField(blank=True, null=True)#
    extraText = models.CharField(max_length=600, blank=True, null=True)#

   
    def create_blank_post():
        post = Post()
        if Category.objects.filter(name="others").exists():
            category = Category.objects.get(name="others")
        else:
            category = Category.objects.create(name="others", linkName="andere", order=99, active=False)
        post.category=category
        post.template = Template.objects.last()
        post.linkName = "Post " + str(post.id)
        post.title = "titel"
        post.save()
        return post


