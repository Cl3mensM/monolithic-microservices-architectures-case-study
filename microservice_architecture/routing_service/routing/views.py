from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def ingress_test_view(request):
    return HttpResponse("✅ You have reached the Routing Service through the Ingress!")
