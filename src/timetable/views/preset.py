from django.shortcuts import render

def preset(request):
    return render(request, 'preset.html')