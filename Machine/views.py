# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import commands

def coding(request):
    return render(request, "coding.html")


def result(request):
    coding_Text = request.POST.get('Coding_Text', '')
    #print coding_Text
    if coding_Text:
        fp = open("a.out", "w")
        fp.write("")
        fp.close()
        fp = open("rock.cpp", "w")
        fp.write(coding_Text)
        fp.close()
        debug_gap = "debug : " + commands.getoutput('g++ rock.cpp')
        ans_gap = "result : " + commands.getoutput('./a.out')
        #print coding_Text
        return render(request, "result.html", {'Text': coding_Text, 'Debug': debug_gap, 'Ans': ans_gap, })
    else:
        return render(request, "result.html", {'Text': 'Not available', })
