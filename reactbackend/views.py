
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from . categories import categories as selfSerializedCats
from . models import Category, Template, Post, Link, Image
from . serializers import CategorySerializer, TemplateSerializer, PostSerializer, LinkSerializer

from . categories import get_images_serialized, get_mainImage_serialized


class MainContext():
    keys = {
        "categories":"categories",
        "category":"category",
        "templates":"templates",
        "template":"template",
        "post": "post",
        "postLinks":"postLinks",
        "mainImage":"mainImage",
        "postImages":"postImages",
        "availableLinks":"availableLinks",
        "is_template": "is_template", #template or category
        "availableImages":"availableImages",
    }


class BackAndFront(MainContext):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_categories(request):
        self = BackAndFront()
        categories = selfSerializedCats()
        return Response({self.keys["categories"]: categories})



class BackOnly(MainContext):
    #Posts
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_post_choices(request):
        self=BackOnly()
        categories = CategorySerializer(Category.objects.all(), many=True).data
        templates = TemplateSerializer(Template.objects.all(), many=True).data
        return Response({
            self.keys["categories"]:categories,
            self.keys["templates"]: templates,
        })

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def toggle_post_active(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.data["postId"])
        active = request.data["active"]
        post.active = active
        post.save()
        return Response({
            self.keys["post"]:PostSerializer(post).data,
            })    


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def edit_post_basics(request):
        self=BackOnly()
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

        return Response({
            self.keys["post"]:post,
            "template":template,
            "category":category,
        })


    # Template und Category
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def change_template_or_category(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.data["postId"])
        change = request.data["change"]
        if change == "template":
            post.template = Template.objects.get(pk=request.data["changeId"])
            is_template = True
        if change == "category":
            post.category = Category.objects.get(pk=request.data["changeId"])
            is_template = False
        post.save()
        
        return Response({
            self.keys["post"]:PostSerializer(post).data,
            self.keys["category"]: CategorySerializer(post.category).data,
            self.keys["template"]: TemplateSerializer(post.template).data,
            self.keys["is_template"]:is_template,
            })    


    #Links
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def add_new_link(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.data["postId"])
        newLinkName = request.data["newLinkName"]
        newLinkHref = request.data["newLinkHref"]
        link = Link.objects.create(name=newLinkName, href=newLinkHref)
        post.links.add(link)
        post.save()
        return Response({
            self.keys["post"]: PostSerializer(post).data,
            self.keys["postLinks"]: LinkSerializer(post.links.all(), many=True).data,
            self.keys["availableLinks"]: Helperz.return_available_links(post.id),
        })


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def remove_link_from_post(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.data["postId"])
        link = Link.objects.get(pk=request.data["linkId"])
        post.links.remove(link)
        post.save()
        return Response({
            self.keys["post"]: PostSerializer(post).data,
            self.keys["availableLinks"]: Helperz.return_available_links(post.id),
            self.keys["postLinks"]: LinkSerializer(post.links.all(), many=True).data,
        })


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def add_link_to_post(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.data["postId"])
        link = Link.objects.get(pk=request.data["linkToAddId"])
        post.links.add(link)
        post.save()
        return Response({
            self.keys["post"]: PostSerializer(post).data,
            self.keys["postLinks"]: LinkSerializer(post.links.all(), many=True).data,
            self.keys["availableLinks"]: Helperz.return_available_links(post.id),
        })

    #Images
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_available_images(request):
        self=BackOnly()
        post = Post.objects.get(pk=request.GET.get("postId"))
        availableImages = Helperz.return_available_images(post)
        return JsonResponse({self.keys["availableImages"]:availableImages})


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def add_or_remove_post_image(request):
        self=BackOnly()
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
        availableImages = Helperz.return_available_images(post)
        post = PostSerializer(post).data
        return JsonResponse({
            self.keys["post"]:post,
            self.keys["postImages"]:postImages,
            self.keys["availableImages"]: availableImages
            })


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def set_main_image(request):
        self=BackOnly()
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
            self.keys["mainImage"]: image,
            self.keys["postImages"]: get_images_serialized(post)
            
        })

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_available_links(request):
        self=BackOnly()
        postId = request.GET.get("postId")
        availableLinks = Helperz.return_available_links(postId)
        return JsonResponse({
            self.keys["availableLinks"]: availableLinks,
        })



class Helperz():
    def return_available_links(postId):
        post = Post.objects.get(pk=postId)
        allLinks = Link.objects.all()
        Links=[]
        for link in allLinks:
            if link not in post.links.all():
                Links.append(link)
        availableLinks = LinkSerializer(Links, many=True).data
        return availableLinks

    def return_available_images(post):
        image = Image.objects.all()
        Images = []
        for i in image:
            if not i in post.images.all() and i != post.mainImage:
                obj = {
                    "id": i.id,
                    "title":i.title,
                    "src": settings.BASEURL + "/static/"+i.src,
                }
                Images.append(obj)
        return Images