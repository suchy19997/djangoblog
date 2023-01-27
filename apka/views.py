from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    #posts=Post.objects.all()
    posts=Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request, 'apka/post_list.html', {'posts': posts})

def VR(request):

    return render(request, 'apka/VR.html', )

# Create your views here.
