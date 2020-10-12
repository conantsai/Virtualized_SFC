from django.shortcuts import render
from board.views import dpiip

def ntopng(request):
    return render(request, 'ntopng.html',{})