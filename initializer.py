import os
import sys
from termcolor import cprint
from pathlib import Path
import base64

files_to_create = ['config.properties']
folders_to_create = ['scripts']
sample = 'bmFtZTogR2V0IHVzZXIKCnByZUFjdGlvbjogCiAgc2NyaXB0OiB8CiAgICBpbXBvcnQgZnVuY3Rpb25zCiAgICBwcmludCgiaGVsbG8gd29ybGQiLCBjb250ZXh0LnRoaXNbJ3JlcXVlc3QnXVsndXJsJ10pCiAgICBmdW5jdGlvbnMuZG8oKQoKcG9zdEFjdGlvbjogCiAgc2NyaXB0OgogICAgZmlsZTogc2NyaXB0cy9wb3N0LnB5CgoKcmVxdWVzdDoKICByZXF1ZXN0VHlwZToganNvbgogIHJlc3BvbnNlVHlwZToganNvbgogIG1ldGhvZDogZ2V0CiAgdXJsOiAie3t2OjpzZXJ2ZXJ9fS9hcGkvdXNlcnMvMiIKICBoZWFkZXJzOgogICAgYXNkYSA6IGFzZGFzZAogICAgcXdlYWFzZDogYXNkZGFzZAogIGJvZHk6IHwKICAgIHsKICAgICAgImFzZCIgOiAiYXNkYXNkIgogICAgfQphc3NpZ246CiAgZnJvbUJvZHk6CiAgICB1c2VyX2lkOiAiJC5kYXRhLmlkIgogICAgdXNlcl9lbWFpbCA6ICIkLmRhdGEuZW1haWwiCiAgZnJvbUhlYWRlcnM6CiAgICBkYXRlOiAiZGF0ZSI='
root = os.getcwd()

def touch_files():
    for f in files_to_create:
        fpath = root + '/' + f
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

def update_config():
    with open(root + '/config.properties', '+a') as f :
        f.write('scripts_dir=scripts')
    


def check_if_init():
    if not '-i' in sys.argv[1:]:
        return
    for x in sys.argv[1:]:
        if('-e' in x):
            for f in x.split('=')[1].split(','):
                files_to_create.append(f + '.properties')
    touch_files()
    create_dir()
    copy_sample()
    update_config()
    exit()


