#!/bin/bash
# Vercel build step: collect static files into staticfiles_build/static.
# The build image's system Python is externally managed (uv/PEP 668), so we
# install Django into a throwaway virtualenv just to run collectstatic.
set -e

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py collectstatic --noinput --clear
