import os

class Directory():

    def __init__(self, dir):
        self.dir = dir

    def __getitem__(self, key):
        #so, we need to find the file in the directory. //how do i want to return this. just as file to work with 
        pass

    def keys(self):
        return os.listdir(self.dir)

