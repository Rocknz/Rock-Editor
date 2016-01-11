# -*- coding: utf-8 -*-

# Folder finder
import os

from django.shortcuts import render

from Engine.models import LatestFolderPath
from Engine.view_dir.views import check_user_auth


def get_guest_url():
    path = os.getcwd()+"/Guest"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def find_folder(request):
    if request.user.is_authenticated():
        path = folder_get_path(request.POST.get('path', ''), request)
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

        if not os.path.exists(path):
            return goto_find_folder(request, get_guest_url(), 'Path is wrong')

       # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return goto_find_folder(request, get_guest_url(), 'Not authorized')

        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        LatestFolderPath.objects.filter(user_id=request.user.get_username()).delete()
        new_data = LatestFolderPath(user_id=request.user.get_username(), path=path)
        new_data.save()

        return render(request, "folder/find_folder.html", {'Path': path, 'Folders': folders, 'Files': files})
    else:
        return render(request, "invalid.html", {})


def folder_get_path(path, request):
    if path == '':
        # get latest url
        try:
            path = LatestFolderPath.objects.get(user_id=request.user.get_username()).path
        except LatestFolderPath.DoesNotExist:
            path = ''

        if path == '':
            path = get_guest_url()

    return path


def make_folder(request):
    if request.user.is_authenticated():
        path = request.POST.get('path', '')
        type = request.POST.get('type', '')

        if path == '' or not os.path.exists(path):
            return goto_find_folder(request, path, 'Path is wrong')
        # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return goto_find_folder(request, path, 'Not authorized')

        new_folder = request.POST.get('new_folder', '')

        if 'new_folder' not in request.POST:
            if type == 'folder':
                btn_name = "Make new folder"
                example = "name"
            else:
                btn_name = "Make new file"
                example = "name.cpp"
            return render(request, "folder/make_folder.html", {'Path': path, 'Btn_name': btn_name, 'Type': type, 'Example': example})
        else:
            if new_folder == '':
                return goto_find_folder(request, path, 'Input is null');

            if os.path.exists(path+"/"+new_folder):
                return goto_find_folder(request, path, 'The folder/file is already exists')

            if type == 'folder':
                new_path = path + "/" + new_folder
                os.makedirs(new_path)
                return goto_find_folder(request, new_path, 'The folder is made')
            else:
                new_path = path + "/" + new_folder
                fp = open(new_path, "w")
                fp.close()
                return goto_find_folder(request, path, 'The file is made')
    else:
        return render(request, "invalid.html", {})


def delete_folder(request):
    if request.user.is_authenticated():
        delete_path = request.POST.get('delete_path', '')
        path = request.POST.get('path', '')
        if path == '' or not os.path.exists(path):
            return goto_find_folder(request, path, 'Path is wrong')

        # check the authorization
        if not check_user_auth(path, request.user.get_username()):
            return goto_find_folder(request, path, 'Not authorized')

        if delete_path == '':
            return goto_find_folder(request, path, 'Delete_path')
        else:
            # check the authorization
            if not check_user_auth(delete_path, request.user.get_username()):
                return goto_find_folder(request, path, 'Not authorized')
            if not os.path.exists(delete_path):
                return goto_find_folder(request, path, 'Deleting Path is wrong')

            # delete
            if os.path.isdir(delete_path):
                for root, dirs, files in os.walk(delete_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(delete_path)
                return goto_find_folder(request, path, 'The folder is deleted')
            else:
                os.remove(delete_path)
                return goto_find_folder(request, path, 'The file is deleted')
    else:
        return render(request, "invalid.html", {})


def goto_find_folder(request, path, noti):
    return render(request, "folder/return_find_folder.html", {'Path': path, 'Noti': noti})
