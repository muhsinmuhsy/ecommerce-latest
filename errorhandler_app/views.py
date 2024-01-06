from django.shortcuts import render

# Create your views here.



def error_404(request, exception):
    return render(request, 'errorhandler/error_404.html', status=404)

def error_500(request):
    return render(request, 'errorhandler/error_500.html', status=500)

def error_403(request, exception):
    return render(request, 'errorhandler/error_403.html', status=403)

def error_400(request, exception):
    return render(request, 'errorhandler/error_400.html', status=400)
