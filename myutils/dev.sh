#!/bin/bash
# for the dev server: fetches new code and restarts the server.

git pull origin master
touch /var/www/emu86_pythonanywhere_com_wsgi.py
