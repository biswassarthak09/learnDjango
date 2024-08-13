from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
def register_user(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Username taken")
                return redirect("register_user")
            elif User.objects.filter(email = email).exists():
                messages.error(request, "Email taken")
                return redirect("register_user")
            else :
                #create User entity
                user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
                #save user to database
                user.save()
                messages.success(request, "User created")
                return redirect("login")
        else :
            messages.error(request, "Password not match")
            return redirect("register_user")

    else :
        return render(request, "register.html")
    

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #authenticate user
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            #login user
            auth.login(request, user)
            return redirect("/")
        else :
            messages.error(request, "Invalid credentials")
            return redirect("login")
    else :
        return render(request, "login.html")
    
def logout_user(request):
    auth.logout(request)
    return redirect("/")

@api_view(['POST'])
def login_user_with_jwt(request):
    username = request.data.get("username")
    password = request.data.get("password")
    #authenticate user
    user = auth.authenticate(username = username, password = password)
    if user is not None:
        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return JsonResponse(tokens)

    else :
        messages.error(request, "Invalid credentials")
        return JsonResponse({'detail': 'Invalid credentials'}, status=400)
