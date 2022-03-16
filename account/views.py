from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {
                "error": "Username and password are not matching"
            })

    return render(request, "account/login.html")


def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html",
                              {
                                  "error": "This username is already taken",
                                  "username": username,
                                  "email": email,
                                  "firstname": firstname,
                                  "lastname": lastname
                              })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html",
                                  {
                                      "error": "This email is already taken",
                                      "username": username,
                                      "email": email,
                                      "firstname": firstname,
                                      "lastname": lastname
                                  })
        else:
            return render(request, "account/register.html",
                          {
                              "error": "Something went wrong",
                              "username": username,
                              "email": email,
                              "firstname": firstname,
                              "lastname": lastname
                          })

    return render(request, "account/register.html")


def logout_request(request):
    logout(request)
    return redirect("/")
