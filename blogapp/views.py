# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .forms import PostForm, CommentForm, RegisterForm
from .models import post
from .serializer import PostSerializer
from .authentication import authenticate_user, jwt_required, generate_jwt_token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.data)  # Use request.data for DRF
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Hash the password
            )

            # Generate JWT token
            token = generate_jwt_token(user)
            return Response({"message": "User registered successfully", "token": token}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:  # GET request
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    token = authenticate_user(username, password)
    if token:
        # Store the token in session for later use
        request.session['token'] = token

        # Redirect to the post creation page
        return HttpResponseRedirect('/posts/create/')
    else:
        return Response({"error": "Invalid credentials"}, status=400)

def index(request):
    return render(request, 'index.html')


# Publicly accessible post list view
@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    posts = post.objects.all().order_by('-created_date')  # Corrected field name
    return render(request, 'post_list.html', {'posts': posts})


# Post creation with JWT authentication required
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
@jwt_required
def post_create(request):
    token = request.session.get('token')  # Get JWT token from session

    if not token:
        return Response({"error": "Not authenticated"}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts-list')
    else:
        form = PostForm()

    return render(request, 'add_post.html', {'form': form})

# Post update with JWT authentication required
@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
@jwt_required
def post_update(request, pk):
    post_instance = get_object_or_404(post, pk=pk)
    if request.method == 'PUT':
        serializer = PostSerializer(post_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:  # GET request
        form = PostForm(instance=post_instance)
        return render(request, 'update_post.html', {'form': form, 'post': post_instance})


@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
@jwt_required
def post_delete(request, pk):
    post_instance = get_object_or_404(post, pk=pk)
    if request.method == 'DELETE':
        post_instance.delete()
        return redirect('posts-list')  # Redirect to the post list after deletion
    return render(request, 'delete_post.html', {'post': post_instance})


# Publicly accessible comment list view
@api_view(['GET'])
@permission_classes([AllowAny])
def comment_list(request, post_pk):
    post_instance = get_object_or_404(post, pk=post_pk)
    comments = post_instance.comments.all()

    return render(request, 'comment_list.html', {'post': post_instance, 'comments': comments})


# Comment creation with JWT authentication required
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
@jwt_required
def comment_create(request, post_pk):
    post_instance = get_object_or_404(post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post_instance
            new_comment.save()
            return redirect('comment-list', post_pk=post_pk)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'post': post_instance})
