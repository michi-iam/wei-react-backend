from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


from ... models import Template, Link, Category, Image, Post
from ... categories import categories as selfSerializedCats
from ... categories import get_images_serialized, get_mainImage_serialized
from ... serializers import PostSerializer, CategorySerializer, ImageSerializer



def get_available_images(request):
    post = Post.objects.get(pk=request.GET.get("postId"))
    availableImages = return_available_images(post)
    return JsonResponse({"availableImages":availableImages})



@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def set_main_image(request):
    imageId = request.data["imageId"]
    postId = request.data["postId"]
    post = Post.objects.get(pk=postId)
    oldMain = post.mainImage
    post.images.add(oldMain)
    image = Image.objects.get(pk=imageId)
    post.mainImage = image
    post.save()
    image = get_mainImage_serialized(post)
    return JsonResponse({
        "mainImage": image,
        "postImages": get_images_serialized(post)
        
    })

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_or_remove_post_image(request):
    imageId = request.data["imageId"]
    postId = request.data["postId"]
    remove = request.data["remove"]

    post = Post.objects.get(pk=postId)
    image = Image.objects.get(pk=imageId)
    if remove:
        post.images.remove(image)
    else:
        post.images.add(image)
    post.save()
    postImages = get_images_serialized(post)
    availableImages = return_available_images(post)
    post = PostSerializer(post).data
    return JsonResponse({
        "post":post,
        "postImages":postImages,
        "availableImages": availableImages
        })


def return_available_images(post):
    image = Image.objects.all()
    Images = []
    for i in image:
        if not i in post.images.all() and i != post.mainImage:
            obj = {
                "id": i.id,
                "title":i.title,
                "src":"http://192.168.178.72:8000/static/"+i.src,
            }
            Images.append(obj)
    return Images



# @api_view(['POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def removeFromPostImage(request):
#     imageId = request.data["imageId"]
#     postId = request.data["postId"]
#     post = Post.objects.get(pk=postId)
#     image = Image.objects.get(pk=imageId)
#     post.images.remove(image)
#     post.save()
#     postImages = get_images_serialized(post)
#     availableImages = return_available_images(post)
#     post = PostSerializer(post).data
#     return JsonResponse({
#         "post":post,
#         "postImages":postImages,
#         "availableImages": availableImages
#         })

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def addToPostImage(request):
#     imageId = request.data["imageId"]
#     postId = request.data["postId"]
#     post = Post.objects.get(pk=postId)
#     image = Image.objects.get(pk=imageId)
#     post.images.add(image)
#     post.save()
#     postImages = get_images_serialized(post)
#     availableImages = return_available_images(post)
#     post = PostSerializer(post).data
#     return JsonResponse({
#         "post":post,
#         "postImages":postImages,
#         "availableImages": availableImages
#         })
