import pandas as pd
import os
import docToText

startpath = 'stuff/documents'

def get_folder_structure(startpath):
    global all_files
    all_files = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    print(all_files)

get_folder_structure(startpath)
for file in all_files:
    print(file)
    print(docToText.main(file))