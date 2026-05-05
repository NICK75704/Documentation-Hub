import os
import docToText
import json

start_path = 'stuff/documents'
data_dir = 'stuff/data/'

all_files = []

def get_folder_structure(startpath):
    global all_files
    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    print(all_files)

def chunk(file_name, contents, file_path):
    global data_dir
    split_contents = contents.split(" ")
    for i in range(len(split_contents) -1):
        split_contents[i] = split_contents[i] + " "
        i += 1
    with open(f'{data_dir}/{file_name}.json', 'w') as f:
        data = [file_name, file_path, split_contents]
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_file_name(file):
    split_path = file.split("/")
    file_name_and_extension = split_path[-1]
    file_name_and_extension = file_name_and_extension.split(".")
    file_name = file_name_and_extension[0]
    file_name = file_name.replace(" ", "-")
    return file_name

get_folder_structure(start_path)

for file in all_files:
    contents = docToText.main(file)
    file_name = get_file_name(file)
    # print(document)
    chunk(file_name, contents, file)