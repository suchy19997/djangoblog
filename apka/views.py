from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from apka.forms import ImgForm
from django.views.generic import DetailView
from django.views.generic import TemplateView


class Image(TemplateView):
    form=ImgForm
    template_name = 'apka/Image.html'

    def post(self,request, *args,**kwargs):
        form = ImgForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('Image_Display', kwargs={'pk':obj.id}))

        context = self.get_contaxt_data(form=form)
        return self.render_to_response(context)

    def get(self,request, *args, **kwargs):
        return self.post(request,*args, **kwargs)

class ImageDisplay(DetailView):
    model = Post
    template_name = 'apka/Image_Display.html'
    context_object_name = 'Image'


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
