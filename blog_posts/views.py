from django.shortcuts import render
from rest_framework import serializers
from .models import BlogPost
from users.models import User
from .serializers import BlogPostSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog_post_view(request):
    try:
        user = User.objects.get(id=request.user.id)
    except:
        data = {
            'status':False,
            'message': 'Invalid token provided',
            'data':[]
        }
        return Response(data,401)
    blog_post = BlogPost(author=user)
    serializer = BlogPostSerializer(blog_post,data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            'status':True,
            'message':'Success! Post created',
            'data':[
                serializer.data
            ]
        }
        return Response(data,201)
    error_msg = get_error_msg(serializer)
    data = {
        'status' : False,
        'message' : error_msg
    }
    return Response(data,400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = BlogPost.objects.filter(author_id=request.user.id)
    serializer = BlogPostSerializer(posts,many=True)
    data = {
        'status':True,
        'message':'Success! Record found',
        'data' : [{
            'posts' : serializer.data
        }]
    }
    return Response(data,200)
    

def get_error_msg(serializer):
    errors = []
    for key,error_msg in serializer.errors.items():
        errors.append(error_msg[0])
    error_msg = 'All fields are required' if 'This field is required.' == errors[0] else errors[0]
    return error_msg