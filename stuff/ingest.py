import os
import docToText
import json

start_path = 'stuff/documents'
data_dir = 'stuff/data/'

all_files = []
chunk_size = 150

def get_folder_structure(startpath):
    global all_files
    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    print(all_files)

def chunk(file_name, contents, file_path, chunk_size = 300):
    global data_dir
    
    words = contents.split()

    split_contents = []
    for i in range(0, len(words), chunk_size):
        chunk_segment = words[i : i + chunk_size]
        split_contents.append(" ".join(chunk_segment))

    data = {
        "metadata": {
            "file_name": file_name,
            "file_path": file_path
        },
        "content": 
            split_contents
    }

    with open(f'{data_dir}/{file_name}.json', 'w') as f:
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
    chunk(file_name, contents, file, chunk_size)