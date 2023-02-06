from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post,Profile_data
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .forms import PostForm, SignUpForm, ProfileForm


def post_list(request):
    #posts=Post.objects.all()
    posts=Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request, 'apka/post_list.html', {'posts': posts})

def VR(request):
    return render(request, 'apka/VR.html', )

def post_detail(request,pk):
    post=get_object_or_404(Post,pk= pk)
    return render(request,'apka/post_detail.html',{'post':post})
# Create your views here.

def error_404_view(request,exception):
    data = {"name": 'BłĄD 404 ośnież stronę'}
    return render(request, 'apka/404.html',data)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'apka/post_edit.html',{'form': form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'apka/post_edit.html',{'form': form})

def sign_up(request):

    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    else:
        form = SignUpForm()
    return render(request, 'apka/sign_up.html', {'form': form})
    #

def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowałeś się.")
    return redirect('/')
def profile_edit(request,pk):

    profile = get_object_or_404(Profile_data, pk=pk)
    print(profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        #form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            profile = form.save(commit=False)

            profile.save()
            return redirect('profile_edit', pk=Profile_data.user)
    else:
        form = ProfileForm(instance=Profile_data)
    #return render(request, 'apka/post_edit.html', {'form': form})
    return render(request, 'apka/profile_edit.html',{'form': form})