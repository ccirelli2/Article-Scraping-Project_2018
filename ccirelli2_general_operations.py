import os

def write_to_excel(dataframe, filename):
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()
    
def write_to_text_file(Text_2_write, File_name2_use):
    file = open(str(File_name2_use) + '.txt', 'w')    
    file.write(Text_2_write)   

    
def write_to_cvs(dataframe, filename):
    writer = pd.DataFrame.to_csv(filename+'.xlsx')
    dataframe.to_excel(writer, 'Data')
    writer.save()

def get_text_files(Dir_list):
    Cwd = os.getcwd()
    Text_list = []
    for name in Dir_list:
        Dir = Cwd + '/' + name
        File = open(Dir, 'rb')
        Text = File.read()
        Text_list.append(Text)    
    return Text_list

def get_File_dir_list():
    Cwd = os.getcwd()
    File_names = os.listdir()

    Dir_list = []
    for name in File_names:
        Dir = Cwd + '/' + name
        Dir_list.append(Dir)
    return Dir_list

