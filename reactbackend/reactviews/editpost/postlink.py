from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from ...models import Post, Template, Category, Link
from ...serializers import PostSerializer, TemplateSerializer, CategorySerializer, LinkSerializer

def return_available_links(postId):
    post = Post.objects.get(pk=postId)
    print(post.links.all())
    allLinks = Link.objects.all()
    Links=[]
    for link in allLinks:
        if link not in post.links.all():
            Links.append(link)

    print(Links)
    availableLinks = LinkSerializer(Links, many=True).data
    return availableLinks


def get_available_links(request):
    postId = request.GET.get("postId")
    availableLinks = return_available_links(postId)
    return JsonResponse({
        "availableLinks": availableLinks,
    })

def get_post_links(request):
    postId = request.GET.get("postId")
    post = Post.objects.get(pk=postId)
    postLinks = LinkSerializer(post.links.all(), many=True).data
    return JsonResponse({
        "postLinks":postLinks
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_new_link(request):
    print(request.data)
    post = Post.objects.get(pk=request.data["postId"])
    newLinkName = request.data["newLinkName"]
    newLinkHref = request.data["newLinkHref"]
    link = Link.objects.create(name=newLinkName, href=newLinkHref)
    post.links.add(link)
    post.save()
    return JsonResponse({
        "post": PostSerializer(post).data,
        "postLinks": LinkSerializer(post.links.all(), many=True).data,
        "availableLinks": return_available_links(post.id),
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def remove_link_from_post(request):
    print(request.data)
    post = Post.objects.get(pk=request.data["postId"])
    link = Link.objects.get(pk=request.data["linkId"])
    post.links.remove(link)
    post.save()
    return JsonResponse({
        "post": PostSerializer(post).data,
        "availableLinks": return_available_links(post.id),
        "postLinks": LinkSerializer(post.links.all(), many=True).data,
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_link_to_post(request):
    post = Post.objects.get(pk=request.data["postId"])
    link = Link.objects.get(pk=request.data["linkToAddId"])
    post.links.add(link)
    post.save()
    return JsonResponse({
        "post": PostSerializer(post).data,
        "postLinks": LinkSerializer(post.links.all(), many=True).data,
        "availableLinks": return_available_links(post.id),
    })