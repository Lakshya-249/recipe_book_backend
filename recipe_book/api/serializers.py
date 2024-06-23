from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Category, Chef, Recipe, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ChefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chef
        fields = ('chef_id','chef_name','email','password','username','url')
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'chef-detail','lookup_field':'pk'}
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id','name','url')
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'pk'}
        }

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    # chef = ChefSerializer(read_only=True)
    # category = CategorySerializer(read_only=True)
    recipe_id = serializers.ReadOnlyField();
    class Meta:
        model = Recipe
        fields = '__all__'

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    # chef = ChefSerializer(read_only=True,many=True)
    # recipe = RecipeSerializer(read_only=True,many=True)
    class Meta:
        model = Review
        fields = ('review_id','comment','chef','recipe')