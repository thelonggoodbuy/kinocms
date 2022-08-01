from django.shortcuts import render



def all_users(request):
    return render(request, 'cinema/all_users.html')