# -*- coding: utf-8 -*-
import codecs
import os
import subprocess
import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render
import commands


def check_user_auth(now_path, user_name):
    guest_path = os.getcwd()+"/Guest"
    if(user_name != "admin") and (guest_path not in now_path):
        return False
    return True


# Folder source open and fix it.
def coding(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '.')

        # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return render(request, "invalid.html", {})

        text = ""
        try:
            fp = codecs.open(path, "r", "utf-8")
            for gap in fp.read():
                text += gap
            fp.close()
        except IOError:
            text = "Not Readable"

        # find extension
        div_path = path.split("/")
        file_name = div_path[div_path.__len__() - 1]
        points = file_name.split('.')
        if points.__len__() != 1:
            ext = points[points.__len__() - 1]
        else:
            ext = "No extension"

        # set the type of codemirror ... normal setting is c or c++
        ext_link = []
        mode = 'text'
        if ext == "py":
            ext_link = ['codemirror/mode/python/python.js']
            mode = 'text/x-python'
        elif ext == "js":
            ext_link = ['codemirror/mode/javascript/javascript.js']
            mode = 'text/javascript'
        elif ext == "css":
            ext_link = ['codemirror/mode/css/css.js']
            mode = 'text/css'
        elif ext == "html" or ext == "xml":
            ext_link = ['codemirror/mode/xml/xml.js', 'codemirror/mode/htmlmixed/htmlmixed.js']
            mode = 'text/html'
        elif ext == "cpp" or ext == "c":
            ext_link = ['codemirror/mode/clike/clike.js']
            mode = 'text/x-c++src'
        elif ext == "php":
            ext_link = ['codemirror/mode/php/php.js', 'codemirror/mode/xml/xml.js', 'codemirror/mode/clike/clike.js']
            mode = 'application/x-httpd-php'
        return render(request, "coding.html", {'Path': path, 'Text': text, 'Ext': ext, 'Ext_Link': ext_link, 'Mode': mode, 'File_name': file_name})
    else:
        return render(request, "invalid.html", {})


# Save the source of fixing code.
def result(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '')

        # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return render(request, "invalid.html", {})

        source = request.POST.get('coding_Text', '')
        ext = request.POST.get('ext', '')
        is_saved = save_file(path, source)
        path = path.replace(" ", "\\ ")
        if source and is_saved == 'Saved':
            if ext == 'c' or ext == 'cpp':
                commands.getoutput('rm a.out')
                run_result = command_time_limit('g++ ' + path, 1)
                if run_result == "Running Error":
                    run_result = ""
                # run
                run_result = run_result + "\n" + command_time_limit('./a.out', 1)
            elif ext == 'py':
                run_result = command_time_limit('python ' + path, 1)
            else:
                run_result = "This type of extension is not runnable"
            return render(request, "result.html", {'Result': run_result})
        else:
            return render(request, "result.html", {'Result': 'Not available'})
    else:
        return render(request, "invalid.html", {})


def command_time_limit(cmd, time_limit):
    def target():
        global process, Ans, Err
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        Ans, Err = process.communicate()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(time_limit)

    if thread.is_alive():
        process.terminate()
        thread.join()
        return "Time is Over"
    if Ans:
        return "Success\n" + Ans
    if Err:
        return "Error\n" + Err
    return "Running Error"


# Main .. init path must be added..
def main(request):
    if request.user.is_authenticated():
        return render(request, "main.html")
    else:
        return HttpResponseRedirect("/")


def save(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '')

        # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return render(request, "invalid.html", {})

        coding_text = request.POST.get('coding_Text', '')
        is_saved = save_file(path, coding_text)
        return render(request, "save.html", {'ANS': is_saved})
    else:
        return render(request, "invalid.html", {})


def save_file(path, text):
    if path != '':
        try:
            fp = codecs.open(path, "r", "utf-8")
            fp.read()
            fp.close()
            fp = codecs.open(path, "w", "utf-8")
            fp.write(text)
            fp.close()
            return 'Saved'
        except IOError:
            return 'Not saved, Path is not permitted'
    return 'Not saved, Path is Null'
