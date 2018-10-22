from django.shortcuts import render, HttpResponse, redirect

from .models import User

from django.contrib import messages

import bcrypt

# Create your views here.
def index(request):
    # if already logged in, don't show login/reg page
    if 'userid' in request.session:
        return redirect('/success')

    # If this is the first visit to this form, put empty values to the context items that will be used in the form
    if 'errors' not in request.session:
        request.session['errors'] = {}
        request.session['form_data'] = {
            'first_name': "",
            'last_name': "",
            'email': "",
        }
    if 'login_error' not in request.session:
        request.session['login_error']=None

    # send in context the error messages (a dictionary where the keys are the fields and the values are the messages) and the previously entered (incorrect) form data

    context = {
        'errors': request.session['errors'],
        'partial': request.session['form_data'],
        'login_error': request.session['login_error']
    }
    request.session.clear()
    return render(request, "login_registration/index.html", context)

def success(request):
    if 'userid' in request.session:
        
        context={
            'user': User.objects.get(id=request.session['userid'])

        }
        return render(request, "login_registration/success.html", context)
    messages.error(request, "You need to login to access this amazing website. Do it... You know you want to!")
    return redirect('/')

def register(request):
    if request.method=="POST":
        # If there are invalid fields, send back to the form, with error messages

        request.session['errors'] = User.objects.basic_validator(request.POST)

        if len(request.session['errors']) > 0:
            request.session['form_data'] = request.POST
            return redirect('/')

        # Hash password:
        hash_pass=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        
        # create new user
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_pass.decode(),
        )
        request.session.clear()
        messages.success(request,"You've been successfully registered.")
        request.session['userid']=User.objects.get(email=request.POST['email']).id
        
        
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == "POST":
        query = User.objects.filter(email=request.POST['email'])
        print(query)
        if len(query)>0:
            user=query[0]
            # Check hashed passwords match
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session.clear()
                request.session['userid']=user.id
                return redirect('/success')
        request.session['login_error'] = "The login and password combination did not match any user. Check your credentials. Wait a minute... Are you trying to sneak in? CUT IT OUT, you hacker wannabe!"
    return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')
