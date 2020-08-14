from django.shortcuts import render
from rest_framework import serializers
from .models import BlogPost
from users.models import User
from .serializers import BlogPostSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication



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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_detail_view(request,slug=None):
    try:
        post = BlogPost.objects.get(slug=slug)
    except:
        data = {
            'status':False,
            'message':'Opps! Record not found'
        }
        return Response(data,404)
    post = BlogPostSerializer(post).data
    data = {
        'status': True,
        'message':'Success! Post found',
        'data':[{
            'post':post
        }]
    }
    return Response(data,200)

@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def update_post_detail_view(request,slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DOES_NOT_EXIST:
        data = {
            'status':False,
            'message':'Opps! Record not found'
        }
        return Response(data,404)
    if blog_post.author_id != request.user.id:
        data = {
            'status':False,
            'message':'Sorry you do not have permission'
        }
        return Response(data,403)
    if request.method == 'DELETE':
        blog_post.delete()
        data = {
            'status':True,
            'message':'Success! Record deleted'
        }
        return Response(data,200)
    if request.method == 'PUT':
        blogpsot_serializer = BlogPostSerializer(blog_post,data=request.data)
        if blogpsot_serializer.is_valid() == False:
            error_msg = get_error_msg(blogpsot_serializer)
            data = {
                'status':False,
                'message':error_msg
            }
            return Response(data,400)
        blogpsot_serializer.save()
        data = {
            'status':True,
            'message':'Success! Post updated',
            'data' : [{
                'post' : blogpsot_serializer.data 
            }]
        }
    return Response(data,200)



def get_error_msg(serializer):
    errors = []
    for key,error_msg in serializer.errors.items():
        errors.append(error_msg[0])
    error_msg = 'All fields are required' if 'This field is required.' == errors[0] else errors[0]
    return error_msg

class BlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_class = (IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return BlogPost.objects.filter(author_id=self.request.user.id)
