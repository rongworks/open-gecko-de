# -*- coding: utf-8 -*-
import yaml
import io
import os
import sys
import shutil
import subprocess

pkg_file = "../conf/packages.yml"
repositories = {}
executives = []
def read_packages(data):
    res = []
    for package in data['packages']:
        pkg = data.get('packages').get(package)
        repo = pkg['repository']
        name = package
        if repo in repositories and pkg['selected'] == True:
            repositories[repo] += ' '+name
        else:
            repositories[repo] = name

# Main
user_home = os.environ.get('HOME','')

with open(pkg_file, 'r') as stream:
    data_loaded = yaml.load(stream)
    #print(data_loaded)
    #print("---------")

    packages = read_packages(data_loaded)
    for repo_name in data_loaded.get('repositories'):
      repo = data_loaded.get('repositories').get(repo_name)
      cmd = repo['command']
      packages = repositories[repo_name].split(' ')
      for package in packages:
        executives.append(cmd+' '+package)
    do_install = input('Install packages? (yes or no)')
    if  do_install == 'y' or do_install == 'yes':
      for exe in executives:
        subprocess.run(exe)
      # Copy config files .. TODO: copy only used config
      if user_home == '':
        user_home = '/home/'+input('User HOME undefined? Please enter username')
      shutil.copy('../dist/.config', user_home+'/.config')
    else:
      for exe in executives:
        print('==== DRY-RUN ====')
        print(exe)
      print('config would be copied to: '+user_home)
