from django.shortcuts import render

def pedido_view(request):
    return render(request, 'pedido\pedido.html')

# Create your views here.
