from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from ...models import Post, Template, Category
from ...serializers import PostSerializer, TemplateSerializer, CategorySerializer

   # categories 
      # templates
      # links
      # order
      # active
      # linkname
# def get_post_choices(request):
#     categories = CategorySerializer(Category.objects.all(), many=True).data
#     templates = TemplateSerializer(Template.objects.all(), many=True).data
#     return JsonResponse({
#         "categories":categories,
#         "templates": templates,
#     })



# @api_view(['POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def edit_post_basics(request):
#     postId = request.data["postId"]
#     if postId == "newPost":
#         post = Post.create_blank_post()
#         print("NEUER POST")
#     else:
#         post = Post.objects.get(pk=postId)
   
#     title = request.data["title"]
#     subTitle = request.data["subTitle"]
#     text = request.data["text"]
#     extraText = request.data["extraText"]
#     linkName = request.data["linkName"]

#     post.title=title
#     post.subTitle=subTitle
#     post.text=text
#     post.extraText=extraText
#     post.linkName =linkName
#     template = TemplateSerializer(post.template).data
#     category = CategorySerializer(post.category).data
#     post.save()


#     post = PostSerializer(post).data

#     return JsonResponse({
#         "post":post,
#         "template":template,
#         "category":category,
#     })

