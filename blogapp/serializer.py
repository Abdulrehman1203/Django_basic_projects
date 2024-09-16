from rest_framework import serializers
from .models import post, comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ['id', 'title', 'author', 'content', 'created_date', 'updated']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ['id', 'post', 'comment_author', 'content', 'created_date']
