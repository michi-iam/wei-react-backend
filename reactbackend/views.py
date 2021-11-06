
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from . categories import categories as selfSerializedCats
from . models import Category, Template, Post
from . serializers import CategorySerializer, TemplateSerializer, PostSerializer


class BackAndFront():
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_categories(request):
        categories = selfSerializedCats()
        return Response({"categories": categories})



class BackOnly():
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_post_choices(request):
        categories = CategorySerializer(Category.objects.all(), many=True).data
        templates = TemplateSerializer(Template.objects.all(), many=True).data
        return Response({
            "categories":categories,
            "templates": templates,
        })

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def toggle_post_active(request):
        post = Post.objects.get(pk=request.data["postId"])
        active = request.data["active"]
        post.active = active
        post.save()
        return JsonResponse({
            "post":PostSerializer(post).data,
            })    

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def edit_post_basics(request):
        postId = request.data["postId"]
        if postId == "newPost":
            post = Post.create_blank_post()
            print("NEUER POST")
        else:
            post = Post.objects.get(pk=postId)
            linkName = request.data["linkName"]
            post.linkName =linkName
    
        title = request.data["title"]
        subTitle = request.data["subTitle"]
        text = request.data["text"]
        extraText = request.data["extraText"]

        post.title=title
        post.subTitle=subTitle
        post.text=text
        post.extraText=extraText
        
        template = TemplateSerializer(post.template).data
        category = CategorySerializer(post.category).data
        post.save()


        post = PostSerializer(post).data

        return JsonResponse({
            "post":post,
            "template":template,
            "category":category,
        })