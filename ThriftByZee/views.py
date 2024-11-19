from django.shortcuts import redirect, render


def home(request):
    return render(request, "home.html")



def about(request):
    return render(request, "about.html")

def support(request):
    return render(request, "support.html")