from django.utils.safestring import mark_safe
from django.conf import settings


from .. models import Template, Link, Category, Image, Post
from .. serializers import TemplateSerializer, CategorySerializer, LinkSerializer


staticUrl = settings.BASEURL+"/static/"

def get_images_serialized(post):
    p=post
    Images = []
    for i in p.images.all():
        if i != p.mainImage:
            imgObj = {
                "id":i.id,
                "src": staticUrl +i.src,
                "alt":i.alt,
                "slideTitle": i.slideTitle,
                "slideText": i.slideText,
            }
            Images.append(imgObj)
    return Images

def get_mainImage_serialized(post):
    p = post
    obj = {}
    if p.mainImage:
        obj = {
                "id":p.mainImage.id,
                "src": staticUrl + p.mainImage.src,
                "alt":p.mainImage.alt,
                "slideTitle": p.mainImage.slideTitle,
                "slideText": p.mainImage.slideText,
                }
    return obj





def categories():
    Categories = []
    categories = Category.objects.all()
    for c in categories:
        Posts=[]
        posts = Post.objects.filter(category=c)
        for p in posts:
            Images = get_images_serialized(p)
            postObj = {
                "id":p.id,
                "category": CategorySerializer(p.category).data,
                "active": p.active,
                "order":p.order,
                "linkName": p.linkName,
                "template": TemplateSerializer(p.template).data,
                "title":p.title,
                "subTitle": p.subTitle,
                "text":mark_safe(p.text),
                "links": LinkSerializer(p.links.all(), many=True).data,
                "mainImage":get_mainImage_serialized(p),
                "images": Images,
                "extraText": p.extraText
            }
            Posts.append(postObj)
        obj = {
            "id": c.id,
            "name": c.name,
            "linkName": c.linkName,
            "order": c.order,
            "posts": Posts,
        }
        Categories.append(obj)
    return Categories
