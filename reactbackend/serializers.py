from rest_framework import serializers
from . models import Template, Link, Category, Image, Post


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"