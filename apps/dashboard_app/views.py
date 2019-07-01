from django.shortcuts import render, redirect 
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'dashboard_app/index.html')


def signIn(request):
    return render(request, 'dashboard_app/signin.html')


def login_user(request):
    data = request.POST
    username_errors = User.objects.validate_username(data)
    pw_errors = User.objects.validate_pw(data)

    if len(username_errors) == 0 and len(pw_errors) == 0:
        try:
            user = User.objects.get(username=data['username'])
            # hash pulled out of db need to be encoded again
            if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                request.session['fname'] = user.fname
                request.session['login'] = True
                request.session['user_id'] = user.id
                return redirect('/dashboard')
            else:
                messages.error(request, 'wrong password!!')
                return redirect('/signin')
        except:
            messages.error(request, 'username does not exists!!')
            return redirect('/signin')
    else:
        if len(username_errors) > 0:
            for k, v in username_errors.items():
                messages.error(request, v)

        if len(pw_errors) > 0:
            for k, v in pw_errors.items():
                messages.error(request, v)

        return redirect('/signin')



def signup(request):
    return render(request, 'dashboard_app/signup.html')


def success(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'dashboard_app/dashboard.html', context)
    

def register_user(request):
    name_errors = User.objects.validate_name(request.POST)
    email_errors = User.objects.validate_email(request.POST['email'])
    password_errors = User.objects.validate_pw(request.POST)
    username_errors = User.objects.validate_username(request.POST['username'])

    flag = User.objects.filter(email=request.POST['email']).exists()
    if not flag and len(name_errors) < 1 and len(email_errors) < 1 and len(password_errors) < 1 and len(username_errors) < 1:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            username=request.POST['username'],
            password=pw_hash
        )
        print('is this user created?===== ', user.fname)
        request.session['login'] = True
        request.session['fname'] = user.fname
        request.session['user_id'] = user.id
        return redirect('/dashboard')
    else: 
        if len(name_errors) < 1: 
            for k, v in name_errors.items():
                messages.error(request, v)
        if len(email_errors) < 1:
            for k, v in email_errors.items():
                messages.error(request, v)
        if len(password_errors) < 1:
            for k, v in password_errors.items():
                messages.error(request, v)
        if len(username_errors) < 1:
            for k, v in username_errors.items():
                messages.error(request, v)
        return redirect('/signup')



def addUser(request):
    return render(request, 'dashboard_app/add_user.html')


def success(request):
    if 'login' in request.session and request.session['login']:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_messages': Message.objects.all()
        }
        return render(request, 'dashboard_app/dashboard.html', context)
    messages.error(request, 'login first')
    return redirect('/')


def post_msg(request):
    content = request.POST['content']
    user = User.objects.get(id=request.session['user_id'])
    msg = Message.objects.create(message=content, user=user)
    return redirect('/dashboard')


def post_comment(request, id):
    msg = Message.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    comment = Comment.objects.create(
        user=user, message=msg, comment=request.POST['comment'])
    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')

