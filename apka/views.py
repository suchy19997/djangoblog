from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post

from .forms import PostForm


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