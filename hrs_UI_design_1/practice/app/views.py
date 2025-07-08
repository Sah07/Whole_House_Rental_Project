from django.shortcuts import render

def landingpage_view(request):
    return render(request, 'app/landingpage.html')

def aboutus_view(request):
    return render(request, 'app/aboutus.html')

def service_view(request):
    return render(request, 'app/service.html')
