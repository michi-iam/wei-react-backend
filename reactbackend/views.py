from django.shortcuts import render
from django.http import JsonResponse

from . models import Template, Link, Category, Image, Post
from . categories import categories

def get_categories(request):
    return JsonResponse({"data":categories()})


def cats():
    categories = Category.objects.all()
    for c in categories:
        c.posts = Post.objects.filter(category=c)
        