from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Profile
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import PostForm, SignUpForm, ProfileForm, UpdateUserForm

#tokken
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.core.mail import EmailMessage

force_text = force_str

def error_404_view(request,exception):
    data = {"name": 'BłĄD 404 odśnież stronę'}
    return render(request, 'apka/404.html',data)
def post_list(request):
    #posts=Post.objects.all()
    posts=Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request, 'apka/post_list.html', {'posts': posts})
def post_detail(request,pk):
    post=get_object_or_404(Post,pk= pk)
    return render(request,'apka/post_detail.html',{'post':post})
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
        if User.objects.filter(email=form.cleaned_data.get("email")).exists() or User.objects.filter(username=form.cleaned_data.get("username")).exists():
            print("sprawdzono")
            messages.warning(request, "Email już jest używany")
            #form.error_messages("error")
            form = SignUpForm()
            return render(request, 'registration/sign_up.html', {'form': form})
        else:
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.is_active = False


            user.save()
            current_site = get_current_site(request)

            subject = 'Aktywuj konto'

            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=password)
            #login(request, user)
            adress = form.cleaned_data.get('mail')
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)
            email=EmailMessage(subject,message,to=[adress])
            email.send()
            return redirect('activation_sent')

    else:
        form = SignUpForm()

    return render(request, 'registration/sign_up.html', {'form': form})
    #

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'apka/VR.html')

def activation_sent_view(request):
    return render(request, 'registration/acitvation_sent.html')
def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowałeś się.")
    return redirect('/')


def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'profil zaktualizowany')
            return redirect(to='profile_edit')
    else:
        print("abc")
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        print(profile_form)

    return render(request, 'registration/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

def VR(request):
    return render(request, 'apka/VR.html', )

def contact(request):
    return render(request, 'apka/contact.html', )
