from django.shortcuts import render

def ui_build(request):
    return render(request, 'build.html')