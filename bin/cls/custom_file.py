import os

class CustomFile:
    def __init__(self):
        self.src = ''
        self.dst = ''

    def dst_path(self):
        user_home = os.environ.get('HOME','')
        return self.dst.replace('$HOME', user_home).replace('~',user_home,1)

    def src_path(self):
        user_home = os.environ.get('HOME','')
        return self.src.replace('$HOME', user_home).replace('~',user_home,1)   
