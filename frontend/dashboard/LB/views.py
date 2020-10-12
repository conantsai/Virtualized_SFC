from django.shortcuts import render

# Create your views here.
def haproxy(request):
    return render(request, 'haproxy.html',{})
