from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.conf import settings

# importing email message for sending of mails
from django.core.mail import EmailMessage
# Create your views here.

def home(request):
    posts = Blog.objects.all()
    context = {"posts": posts}
    return render(request, 'blog/home.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User(username=username, email=email, password=password)
        new_user.save()
        return redirect("/")
    return render(request, 'blog/signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username is None or password is None:
            messages.info(request, "username or password not found")
            return redirect('/login')
        user= auth.authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Invalid login credentials")
            return redirect('/login')
        auth.login(request, user)
        return redirect('/')
        # print(username , password)
    return render(request, 'blog/login.html')

def logout(request):
    print(request.user)
    auth.logout(request)
    return redirect('/')

@login_required
def create(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
        category = request.POST.get('category')
        context = request.POST.get('context')
        blog_create = Blog.objects.create(title=title, category=category, context=context, author=author)
        blog_create.save()
        return redirect(reverse("home"))
    return render(request, 'blog/create.html')

def read(request,id):
    try:
        post = Blog.objects.get(id=id)
        context = {'post':post}
    except:
        context = {"post":None}
    return render(request, 'blog/read.html', context)


login_required
def delete(request,id):
    post = Blog.objects.get(id=id)
    if post.author == request.user:
        post.delete()
    return redirect(reverse('home'))


login_required
def edit(request,id):
    post = Blog.objects.get(id=id)
    context = {'post':post}
    if post.author != request.user:
        messages.info(request, "you are not authorized")
        return redirect(reverse('home'))
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        img = request.FILES.get('img')
        if img:
            post.image = img
        post.title = title
        post.category = category
        post.content = content
        post.save()

        messages.info(request,"post is edited successfully")
        return redirect(reverse("home"))
    return render(request, 'blog/edit.html', context)


class contact(View):
    def get(self, request):
        return render(request, "blog/contact.html")
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = "Thanks for contacting me"
        body = f"Hello {name},\n\nThank you for reaching out to me, your message has been received successfully, we will get back to you in due time\n\nWarm Regards,\n\nAlade Mayowa\nCEO Mayowa enterprise"

        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [email])
        mail.send()
        
        subject = "New message Alert"
        body = f"A new message was received from {name}, with the message of '{message}', and a mail has been automatically sent to their eamil, which is {email} Please attend to it"
        
        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [settings.EMAIL_HOST_USER])
        mail.send()
        messages.info(request, "Your message was sent successfully")
        return redirect(reverse('home'))




def client_error (request, exception):
    return render(request,"blog/error.html")

def server_error(request):

    return render(request,"blog/server_error.html")







