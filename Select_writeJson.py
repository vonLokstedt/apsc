
import json
from functools import reduce
from operator import getitem
import shutil
import os
import time
def say_JSON(value):
   #print("yay:",value )
   # Data to be written
   dictionary = {
       "file": value[0],
       "statusSelected": value[1],
       "namez_": value[2]
   }

   # with open("selected_.json", "w") as outfile:
     #   json.dump(dictionary, outfile)
def write_json(value, filename='data.json'):
    #print('write:'+value[2])
    with open(filename, 'r+') as file:
           # First we load existing data into a dict.
           file_data = json.load(file)
           # Join new_data with file_data inside emp_details
           dictionary = {
               "file": value[0],
               "statusSelected": value[1],
               "namez_": value[2]
           }
           file_data["photoSelection"].append(dictionary)
           # Sets file's current position at offset.
           file.seek(0)
           # convert back to json.
           json.dump(file_data, file, indent=4)
           file.close()




