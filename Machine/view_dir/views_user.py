# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Machine.view_dir import views


def login_view(request):
    # Session is or not.
    if not request.user.is_authenticated():
        id = request.POST.get('id', '')
        pw = request.POST.get('pw', '')
        if id is '' or pw is '':
            return render(request, "login.html", {'ID': 'guest', 'PW': 'asdf1234', 'NOTI': 'Please Enter id or pw.'})
        else:
            user = authenticate(username=id, password=pw)
            if user is not None:
                login(request, user)
                return views.main(request)
            else:
                return render(request, "login.html", {'ID': id, 'NOTI': 'Disable account.'})
    else:
        return views.main(request)


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect("/")
