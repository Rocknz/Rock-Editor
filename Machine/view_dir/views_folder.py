# -*- coding: utf-8 -*-

# Folder finder
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render


def find_folder(request):
    if request.user.is_authenticated():
        path = folder_get_path(request.POST.get('path', ''))
        order = request.POST.get('order', '')

        # move order..
        if order == 'cd ..':
            splits = path.split('/')
            path = ""
            for line in range(1, splits.__len__()-1):
                path = path + "/" + splits[line]
        elif 'cd' in order:
            if path == '/':
                path = ''
            path = path + "/" + order[3:]

        if path == '':
            path = '/'

        # only admin user can access
        home_path = os.getcwd()+"/Guest"
        if (request.user.get_username() != "admin") and (home_path not in path):
            path = os.getcwd()+"/Guest"

        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        return render(request, "folder/find_folder.html", {'Path': path, 'Folders': folders, 'Files': files})
    else:
        return HttpResponseRedirect("/")


def folder_get_path(path):
    if path == '':
        # get current url
        path = os.getcwd()+"/Guest"
        if not os.path.exists(path):
            os.makedirs(path)
    return path


def make_folder(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '')
        type = request.POST.get('type', '')

        # only admin user can access upper directory of The Guest
        home_path = os.getcwd()+"/Guest"
        if (request.user.get_username() != "admin") and (home_path not in path):
            return HttpResponseRedirect('/')

        new_folder = request.POST.get('new_folder', '')
        if new_folder == '':
            btn_name = ''
            if type == 'folder':
                btn_name = "폴더 생성"
            else:
                btn_name = "파일 생성"
            return render(request, "folder/make_folder.html", {'Path': path, 'Btn_name': btn_name, 'Type': type})
        else:
            if type == 'folder':
                new_path = path + "/" + new_folder
                os.makedirs(new_path)
                return render(request, "folder/make_folder.html", {'Path': new_path, 'Move': 'true'})
            else:
                new_path = path + "/" + new_folder
                fp = open(new_path, "w")
                fp.close()
                return render(request, "folder/make_folder.html", {'Path': path, 'Move': 'true'})
    else:
        return HttpResponseRedirect('/')


def delete_folder(request):
    if request.user.is_authenticated():
        delete_path = request.POST.get('delete_path', '')
        print "delete_path="+delete_path
        path = folder_get_path(request.POST.get('path', ''))
        if delete_path == '':
            # only admin user can delete upper directory of The Guest
            home_path = os.getcwd()+"/Guest"
            if (request.user.get_username() != "admin") and (home_path not in path):
                return HttpResponseRedirect('/')

            folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            return render(request, "folder/delete_folder.html", {'Path': path, 'Folders': folders, 'Files': files})
        else:
            # only admin user can delete upper directory of The Guest
            home_path = os.getcwd()+"/Guest"
            if (request.user.get_username() != "admin") and ((home_path not in path) or (home_path not in delete_path)):
                return HttpResponseRedirect('/')
            # delete
            print "i am here!"
            if os.path.isdir(delete_path):
                for root, dirs, files in os.walk(delete_path, topdown=False):
                    for name in files:
                        print(os.path.join(root, name))
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(delete_path)
            else:
                os.remove(delete_path)
            return render(request, "folder/delete_folder.html", {'Path': path, 'Move': 'true'})
    else:
        return HttpResponseRedirect('/')

