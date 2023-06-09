import os
from time import strftime
from sys import platform, exc_info
import tkinter as tk
from tkinter import filedialog, messagebox

# Counts the number of files in the directory that can be converted
def n_files(directory):
    total = 0
    for file in os.listdir(directory):
        if (file.endswith('.doc') or file.endswith('.docx') or file.endswith('.tmd')):
            total += 1
    return total

# Creates a new directory within current directory called PDFs
def createFolder(directory):
    if not os.path.exists(directory + '/PDFs'):
        os.makedirs(directory + '/PDFs')

def doc2pdf_libreoffice(doc, ending, newdic):
    """
    convert a doc/docx document to pdf format
    :param doc: path to document
    """
    cmd = f"lowriter --convert-to pdf:writer_pdf_Export '{doc}'"
    os.system(cmd)
    if platform == 'win32':
        new_file = new_file.replace("/", "\\")
        cmdmove = f"move '{new_file}' '{newdic}'"
    
    os.system(cmdmove)
    print(new_file)

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

def convert_files(directory):
    # Opens each file with Microsoft Word and saves as a PDF
    try:
        if(is_tool('libreoffice') == False):
            from win32com import client
            word = client.DispatchEx('Word.Application')
        for file in os.listdir(directory):
            if (file.endswith('.doc') or file.endswith('.docx') or file.endswith('.tmd')):
                ending = ""
                if file.endswith('.doc'):
                    ending = '.doc'
                if file.endswith('.docx'):
                    ending = '.docx'
                if file.endswith('.tmd'):
                    ending = '.tmd'
                if is_tool('libreoffice'):
                    in_file = os.path.abspath(directory + '/' + file)
                    new_file = os.path.abspath(directory + '/PDFs')
                    doc2pdf_libreoffice(in_file, ending, new_file)

                if(is_tool('libreoffice') == False):
                    new_name = file.replace(ending,r".pdf")
                    in_file = os.path.abspath(directory + '\\' + file)
                    new_file = os.path.abspath(directory + '\\PDFs' + '\\' + new_name)
                    doc = word.Documents.Open(in_file)
                    print(new_name)
                    doc.SaveAs(new_file,FileFormat = 17)
                    doc.Close()
                
    except Exception as e:
        print(e)

def browse_directory():
    global directory_label, directory_path
    directory_path = filedialog.askdirectory()
    directory_label.config(text=directory_path)

def convert():
    global directory_path
    if n_files(directory_path) == 0:
        messagebox.showwarning('No files', 'There are no files to convert')
        return
    createFolder(directory_path)
    convert_files(directory_path)
    messagebox.showinfo('Conversion complete', 'All files have been converted.')

# Create GUI
root = tk.Tk()
root.title('PDFify')

directory_label = tk.Label(root, text='Please select a directory')
directory_label.pack()

browse_button = tk.Button(root, text='Browse', command=browse_directory)
browse_button.pack()

convert_button = tk.Button(root, text='Convert', command=convert)
convert_button.pack()

root.mainloop()
