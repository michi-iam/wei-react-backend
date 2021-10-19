from . models import Template, Link, Category, Image, Post
from django.utils.safestring import mark_safe
staticUrl = "http://192.168.178.72:8000/static/"

def categories():
    Categories = []
    categories = Category.objects.all()
    for c in categories:
        Posts=[]
        posts = Post.objects.filter(category=c)
        for p in posts:
            Links=[]
            for l in p.links.all():
                linkObj = {
                    "id": l.id,
                    "name":l.name,
                    "href":l.href,
                }
                Links.append(linkObj)
            Images = []
            for i in p.images.all():
                imgObj = {
                    "id":i.id,
                    "src": staticUrl +i.src,
                    "alt":i.alt,
                    "slideTitle": i.slideTitle,
                    "slideText": i.slideText,
                }
                Images.append(imgObj)
            postObj = {
                "id":p.id,
                "order":p.order,
                "linkName": p.linkName,
                "template": p.template.key,
                "title":p.title,
                "subTitle": p.subTitle,
                "text":mark_safe(p.text),
                "links": Links,
                "mainImage":{
                    "id":p.mainImage.id,
                    "src": staticUrl + p.mainImage.src,
                    "alt":p.mainImage.alt,
                    "slideTitle": p.mainImage.slideTitle,
                    "slideText": p.mainImage.slideText,
                },
                "images": Images,
                "seitenText": p.extraText
            }
            Posts.append(postObj)
        obj = {
            "id": c.id,
            "linkName": c.linkName,
            "order": c.order,
            "posts": Posts,
        }
        Categories.append(obj)
    return Categories
