# -*- coding: utf-8 -*-
import yaml
import io
import shutil
import subprocess

pkg_file = "../conf/packages.yml"

def read_packages(data):
    res = []
    for package in data['packages']:
        pkg = data.get('packages').get(package)
        cmd = pkg['command']
        name = package
        selected = pkg['selected']
        if selected == True:
          res.append(cmd+' '+name)
    return res


# Main
with open(pkg_file, 'r') as stream:
    data_loaded = yaml.load(stream)
    print(data_loaded)
    print("---------")

    packages = read_packages(data_loaded)
    for package in packages:
        #subprocess.run(package)
#shutil.copytree(../dist/.config, ~/.config)
