from rest_framework import serializers
from .models import Article, Tag, Comment
from typing import OrderedDict


class ArticleListSerializer(serializers.ListSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'tag', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['user']
        list_serializer_class = ArticleListSerializer

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)



    def to_representation(self, instance: Article) -> OrderedDict:
        representation = super().to_representation(instance)
        representation['tag'] = [tag.title for tag in instance.tag.all()]
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', )
