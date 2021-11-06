from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from ...models import Post, Template, Category
from ...serializers import PostSerializer, TemplateSerializer, CategorySerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def change_template_or_category(request):
      print(request.data)
      post = Post.objects.get(pk=request.data["postId"])
      change = request.data["change"]
      if change == "template":
         print(post.template.id)
         post.template = Template.objects.get(pk=request.data["changeId"])
         is_template = True
      if change == "category":
         post.category = Category.objects.get(pk=request.data["changeId"])
         is_template = False
      post.save()
      
      return JsonResponse({
         "post":PostSerializer(post).data,
         "category": CategorySerializer(post.category).data,
         "template": TemplateSerializer(post.template).data,
         "is_template":is_template,
         })          
      
  
  