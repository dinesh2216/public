# file operations
import os
import datetime

print("welcome to the file operations program here you can read,write and also you can do a alot of stuff ")
print("here are some options you can play with ")
print('''1 creating a file 
2 reading a file 
3 writing a file 
4 check and print the file location of the file and rename of the file
''')
ch = int(input("enter your choice: "))

def fileaccess():
    path = input("enter the path of the file")
    os.chdir(path)
    file = input("enter the name of the file: ")
    fname = file + ".txt"
    return fname

def filecreation():
    path = input("enter the destination of the file to create ")
    os.chdir(path)
    file = input("enter the name of the file: ")
    fname = file + ".txt"
    with open(fname, "w") as file:
        print("file created successfully")
        print("the path of the file", os.path.abspath(fname))
    print('''1 reading a file 
             2 writing a file 
             3 file Updation
            ''')
    option = int(input("enter your choice: "))
    if option == 1:
        filereading(fname)
    elif option == 2:
        fileoverwrite(fname)
    elif option == 3:
        fileupdation(fname)

def filereading(fname):
    with open(fname, "r") as file:
        print(file.read())

def fileupdation(fname):
    with open(fname, "a") as file:
        txt = input(" enter the text you need to update into the file: ")
        file.write(txt)
        filereading(fname)

def fileoverwrite(fname):
    with open(fname, "w") as file:
        txt = input(" enter the text you need to update into the file: ")
        file.write(txt)
        filereading(fname)
   
def filepath(fname):
    return (os.path.abspath(fname))

if ch == 1:
    a = filecreation()
elif ch == 2:
    b = fileaccess()
    a = filereading(b)
elif ch == 3:
    print("1 file updation, 2 file overwrite")
    b = input("enter your choice: ")
    if b == 1:
        a = fileaccess()
        fileupdation(a)
    else:
        a = fileaccess()
        fileoverwrite(a)