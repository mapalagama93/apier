import os
import sys
from termcolor import cprint
from pathlib import Path
import base64
import args

files_to_create = ['config.properties', 'vars.properties']
folders_to_create = ['configs', 'scripts']
sample = 'bmFtZTogR2V0IHVzZXIKCnByZUFjdGlvbjogCiAgc2NyaXB0OiB8CiAgICBpbXBvcnQgZnVuY3Rpb25zCiAgICBwcmludCgiaGVsbG8gd29ybGQiLCBjb250ZXh0LnRoaXNbJ3JlcXVlc3QnXVsndXJsJ10pCiAgICBmdW5jdGlvbnMuZG8oKQoKcG9zdEFjdGlvbjogCiAgc2NyaXB0OgogICAgZmlsZTogc2NyaXB0cy9wb3N0LnB5CgoKcmVxdWVzdDoKICByZXF1ZXN0VHlwZToganNvbgogIHJlc3BvbnNlVHlwZToganNvbgogIG1ldGhvZDogZ2V0CiAgdXJsOiAie3t2OjpzZXJ2ZXJ9fS9hcGkvdXNlcnMvMiIKICBoZWFkZXJzOgogICAgYXNkYSA6IGFzZGFzZAogICAgcXdlYWFzZDogYXNkZGFzZAogIGJvZHk6IHwKICAgIHsKICAgICAgImFzZCIgOiAiYXNkYXNkIgogICAgfQphc3NpZ246CiAgZnJvbUJvZHk6CiAgICB1c2VyX2lkOiAiJC5kYXRhLmlkIgogICAgdXNlcl9lbWFpbCA6ICIkLmRhdGEuZW1haWwiCiAgZnJvbUhlYWRlcnM6CiAgICBkYXRlOiAiZGF0ZSI='
root = os.getcwd()

def touch_files():
    for f in files_to_create:
        fpath = root + '/configs/' + f
        Path(fpath).touch(exist_ok=True)
        cprint('create file ' + fpath, 'green')

def create_dir():
    for f in folders_to_create:
        fpath = root + '/' + f
        Path(fpath).mkdir(exist_ok=True)
        cprint('create folder ' + fpath, 'green')

def copy_sample():
    with open(root + '/sample.yaml', '+a') as f :
        f.write(str(base64.b64decode(sample), encoding='utf-8'))
        cprint('create sample.yaml request', 'green')
    with open(root + '/scripts/functions.py', '+a') as f :
        f.write('import vars\n')
        cprint('create functions.py', 'green')

def update_config():
    with open(root + '/configs/config.properties', '+a') as f :
        f.write('scripts_dir=../scripts')


def init():
    for x in args.env:
        files_to_create.append(x + '.properties')
    create_dir()
    touch_files()
    copy_sample()
    update_config()


