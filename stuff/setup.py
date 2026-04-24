import os

'''makes documentation directory'''
def make_doc_dir():
    try:
        os.mkdir("documents")
        print("Made documents dir...")
    except FileExistsError:
        print("Documents dir already exists!")
    except PermissionError:
        print("Don't have permission to make a new directory")
        exit

'''makes database directory'''
def make_data_dir():
    try:
        os.mkdir("data")
        print("Made data dir...")
    except FileExistsError:
        print("Data dir already exists!")
    except PermissionError:
        print("Don't have permission to make a new directory")
        exit       

make_doc_dir()
make_data_dir()
