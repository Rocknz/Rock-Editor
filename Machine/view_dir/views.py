# -*- coding: utf-8 -*-
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
import commands


# Folder source open and fix it.
def coding(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '.')

        # only admin user to access
        home_path = os.getcwd()+"/Guest"
        if (request.user.get_username() != "admin") and (home_path not in path):
            return HttpResponseRedirect("/")

        text = ""
        try:
            fp = open(path, "r")
            for gap in fp.read():
                text += gap
            fp.close()
        except IOError:
            text = "Not Readable"
        return render(request, "coding.html", {'Path': path, 'Text': text})
    else:
        return HttpResponseRedirect("/")


# Save the source of fixing code.
def result(request):
    if request.user.is_authenticated():
        coding_text = request.POST.get('coding_Text', '')
        if coding_text:
            fp = open("a.out", "w")
            fp.write("")
            fp.close()
            fp = open("rock.cpp", "w")
            fp.write(coding_text)
            fp.close()
            debug_gap = "debug : " + commands.getoutput('g++ rock.cpp')
            ans_gap = "result : " + commands.getoutput('./a.out')
            return render(request, "result.html", {'Text': coding_text, 'Debug': debug_gap, 'Ans': ans_gap})
        else:
            return render(request, "result.html", {'Ans': 'Not available',})
    else:
        return HttpResponseRedirect("/")


# Main .. init path must be..
def main(request):
    if request.user.is_authenticated():
        return render(request, "main.html")
    else:
        return HttpResponseRedirect("/")


def save(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '')
        coding_text = request.POST.get('coding_Text', '')
        if path != '':
            try:
                fp = open(path, "r")
                text = fp.read()
                fp.close()
                fp = open(path, "w")
                fp.write(coding_text)
                fp.close()
                return render(request, "save.html", {'ANS': 'saved'})
            except IOError:
                text=""
        return render(request, "save.html", {'ANS': 'Not saved'})
    else:
        return HttpResponseRedirect("/")
