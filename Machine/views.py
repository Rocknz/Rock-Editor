# -*- coding: utf-8 -*-
import os

from django.shortcuts import render
import commands


# Folder finder
def find_folder(request):
    path = folder_get_path(request.POST.get('path', ''))
    order = request.POST.get('order', '')
    # order = 'cd Machine/Migration'
    # move order..
    if order == 'cd ..':
        splits = path.split('/')
        path = ""
        for line in range(1, splits.__len__()-1):
            path = path + "/" + splits[line]
    elif 'cd' in order:
        if path is '/':
            path = ''
        path = path + "/" + order[3:]

    if path is '':
        path = '/'

    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    return render(request, "find_folder.html", {'Link': path, 'Folders': folders, 'Files': files})


def folder_get_path(path):
    if path is '':
        # get current url
        path = os.getcwd()
    return path


# Folder source open and fix it.
def coding(request):
    path = request.POST.get('path', '.')
    text = ""
    try:
        fp = open(path, "r")
        for gap in fp.read():
            text += gap
        fp.close()
    except IOError:
        text = "Not Readable"
    return render(request, "coding.html", {'Path': path, 'Text': text})


# Save the source of fixing code.
def result(request):
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
        return render(request, "result.html", {'Text': coding_text, 'Debug': debug_gap, 'Ans': ans_gap, })
    else:
        return render(request, "result.html", {'Ans': 'Not available', })


# Main .. init path must be..
def main(request):
    return render(request, "main.html")


def save(request):
    path = request.POST.get('path', '')
    print path
    coding_text = request.POST.get('coding_Text', '')
    if path is not '':
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
