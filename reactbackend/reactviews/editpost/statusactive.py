from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from ...models import Post, Template, Category
from ...serializers import PostSerializer, TemplateSerializer, CategorySerializer


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def toggle_post_active(request):
#       print(request.data)
#       post = Post.objects.get(pk=request.data["postId"])
#       active = request.data["active"]
#       print(post.active)
#       post.active = active
#       post.save()
#       print(post.active)
      
#       return JsonResponse({
#          "post":PostSerializer(post).data,
#          })          
      
  
  