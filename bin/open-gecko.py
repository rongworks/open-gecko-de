# -*- coding: utf-8 -*-
#import yaml
import io
import os
import sys
import shutil
import subprocess
import argparse

from cls.package import Package
from cls.parser import Parser
from cls.custom_file import CustomFile

try:
 import yaml
except ImportError as e:
 print("Yaml package not found, please install python-yaml package")
 exit(1)


class InstallManager:

    def __init__(self):
        self.packages = []
        self.repositories = []
        self.categories = {}
        self.files = []

    def parse_config(self,file):
        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)
            #print(data_loaded)
            #print("---------")

        parser = Parser(data_loaded)
        #repositories = repositories_from_yaml(data_loaded)
        self.packages = parser.read_packages()
        self.files = parser.read_files()
        for package in self.packages:
            if not package.category in self.categories:
                self.categories[package.category] = [package]
            else:
                self.categories[package.category].append(package)

    def list_categories(self):
        for ckey in self.categories:
            cat_pkgs = self.categories[ckey]
            print("===== "+ckey+" =====")
            for package in cat_pkgs:
                print(package.as_string())

    def install_packages(self):
        installable = ["system"]
        for ckey in self.categories:
            if ckey in "system" or input("Install packages from category: "+ckey+"? (yes/no)") in ["y","yes"]:
                installable.append(ckey)
        for ikey in installable:
            cat_pkgs = self.categories[ikey]
            for package in cat_pkgs:
                package.install()
    def install_files(self):
        for cfile in self.files:
          if os.path.isdir(cfile.src_path()):
            try:
              shutil.copyTree(cfile.src,cfile.dst_path())
            except:
              subprocess.call(['sudo','cp -r',cfile.src,cfile.dst_path()])
          else:
            try:
              shutil.copy2(cfile.src,cfile.dst_path())
            except:
              subprocess.call(['sudo','cp',cfile.src,cfile.dst_path()])
    def prepare_config(self,dry):
        if os.path.isdir('../dist'):
            shutil.rmtree('../dist')
            os.makedirs('../dist/open-gecko')
        for package in self.packages:
            package.prepare_config(dry)
        for cfile in self.files:
          if os.path.isdir(cfile.dst_path()):
            shutil.copyTree(cfile.dst_path(),cfile.src_path())
          else:
            shutil.copy2(cfile.dst_path(),cfile.src_path())


# Main
user_home = os.environ.get('HOME','')
app_name = 'Open Gecko DE'
version = '0.5.0'
description = "Installer script for installing custom OpenBox-Desktop\n \
  usage: open-gecko.py COMMAND [PATH]\n \
  COMMANDS: \n \
    info = show this text \n \
    categories = list categories and packages \n \
    install = Install "+app_name+ "\n \
  PATH: \n \
    path = path to config file"

pkg_file = '../conf/packages.yml'

def info():
    print(app_name)
    print(version)
    print(description)
    print('config: '+pkg_file)

def list_categories():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.list_categories()

def install():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.install_packages()
    install_manager.install_files()

def prepare_config():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.prepare_config(False)

command = 'info'
if len(sys.argv) > 1:
    command = command = sys.argv[1]
    if len(sys.argv) > 2:
        pkg_file = sys.argv[2]

if command == 'info':
    info()
elif command == 'categories':
    list_categories()
elif command == 'install':
    install()
    #subprocess.call(['sudo','cp','../dist/open-gecko.desktop','/usr/share/xsessions/open-gecko.desktop'])
elif command == 'prepare_config':
    prepare_config()
else:
   print("Wrong arguments")
   info()
