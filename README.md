
Rock-editor
==============
 **Rock-editor is a cloud editor.** 
 Through this editor, you can make or fix your codes in your server(editor installed). and it assists to control the folders and files in the server. Because It is the cloud editor, you can use this editor anywhere if you have browser (like mobile, tablet). 
 
### Django
Rock-editor is python Django project with html, javascript, jquery.

### Code Mirror
This editor use code-mirror to fix the codes. Codbmirror is open-source text editor implemented in JavaScript for the browser. [pages](https://codemirror.net)

### Bootplus
Boot plus is Google styled front-end framework for faster and easier web development.[pages](http://aozora.github.io/bootplus/)

Usage
------
1) Clone this project
	git clone https://github.com/Rocknz/Rock-Editor.git
2) Install Django
	sudo apt-get install python-django
3) Run Django project wigs through gunicorn or another.
4) Login 
  ID: admin PW: asdf1234
  ID: guest PW: asdf1234
  Change the password of admin.

  guest id : can not access to the upper directory of Rock Editor/Guest.
  admin id : can access all the files in the server.

Support or Contact
------
[email](jrj325@hanmir.com) 
[document](https://github.com/contact) 







app:Machine/view_dir

views.py
 - coding
 - result
 - main
 - save

views_folder.py
 - find_folder
 - make_folder
 - delete_folder

views_user.py
 - login_view
 - logout_view



templates:
: folder/
    - delete_folder
    - find_folder
    - make_folder
 - coding
 - login
 - main
 - result
 - save
