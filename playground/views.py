from django.shortcuts import render

# Create your views here.
def say_hello(request):
    return render(request, "hello.html", {"name": "Minami"})

def add_two_numbers(request):
    x = int(request.POST["num1"])
    y = int(request.POST["num2"])
    result = x + y
    return render(request, "result.html", {"result": result})