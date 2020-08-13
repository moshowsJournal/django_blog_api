from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    #model handles the required fields
    username = serializers.SerializerMethodField('get_author_username_from_blogpost')
    class Meta:
        model = BlogPost
        fields = ['title','body','date_updated','username'] #These are field to be returned
    
    def get_author_username_from_blogpost(self,blog_post):
        return blog_post.author.username

