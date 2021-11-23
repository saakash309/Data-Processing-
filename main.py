from tkinter import *
from database import *
import config
from tkinter import messagebox,Canvas,ttk
import tkinter as tk

global keys
global clms
try:
    ob = config.Data('config.ini')
    fname = ob.fpath()
    keys = ob.fields()
except IndexError:
    messagebox.showerror('File absent','No config file found')
try:
    original_clms= data_columns(keys,fname)
    clms = data_columns(keys,fname)
except FileNotFoundError:
    messagebox.showerror('No file','The file you were looking for is missing')


def clear():
    for entries in box_names:
        entries.delete(0,END)
def update(tree,line):
    tree.insert('',END,values=tuple(line.split(';')))

def value(t):
    x=t.get()
    return x

def save(): 
    line = ''
    for _ in range(len(box_names)):                                              #for empty fields
        if value(box_names[_]).strip() == '':
                messagebox.showerror('Fields empty','Fields cannot be left empty')
                return 
    for _ in range(len(box_names)):
        # print(value(box_names[_]))
        # print(attr_type(value(box_names[_])))
        if attr_type(value(box_names[_]))==temp_list[_]:
            line += value(box_names[_]) + ";"
            response = 'yes'
        else:
            response = messagebox.askquestion('Incorrect data type','The data type you entered dosent matches with the field. Do you still want to add?')
            break
    if response == 'no':
        for entries in box_names:
            entries.delete(0,END)
    else:
        line =''
        for _ in range(len(box_names)):
            line += value(box_names[_]) + ";"
    if line != '':
        add_data(line,fname)
        for entries in box_names:
            entries.delete(0,END)
    else:
        messagebox.showerror('Unexpected Error','Restarting may solve this issue.')
    update(tree,line)

def search():
    #for rows in my_tree.

    for row in my_tree.get_children():
        my_tree.delete(row)
    result = []
    param = search_entry.get()
    object_list = data_columns(keys,fname)
    for object in object_list:
        if getattr(object,'IDNUMBER') == param:
            result.append(object)
    if not result:
        search_entry.delete(0,END)
        messagebox.showerror('No seach results found','No search results were found. You can try with some other values')
        
    for obj in result:
        dummy = ''
        for key in keys:
            dummy += getattr(obj,key) + ';'
        update(my_tree,dummy)


def checker(key,clms):
    temp1=[]
    for j in clms:
        temp1.append(attr_type(getattr(j,key)))
    if 'int' not in temp1:
        return 'str'
    elif 'str' not in temp1:
        return 'int'
    return 'str'

temp_list = []
for i in keys:
    try:
        temp_list.append(checker(i,original_clms))
    except AttributeError:
        temp_list.append('str')
    #saving the value type of each field in a array
def tree_view_frame(keys,clms,frame):
    columns = tuple(keys)
    # tree.grid(row=0, column=0, sticky='nsew')
    # #scrollbar #, orient=tk.VERTICAL, command=tree.yview
    scrollbary = Scrollbar(frame)
    scrollbary.pack(side=RIGHT,fill=Y)
    scrollbarx = Scrollbar(frame,orient=HORIZONTAL)
    scrollbarx.pack(side=BOTTOM,fill=X)
    tree =ttk.Treeview(frame, columns=columns, show='headings',yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
    # define headings
    for i in range(len(keys)):
        tree.heading(keys[i],text=keys[i],anchor=CENTER)
    #     tree.column(keys[i], anchor=CENTER, width=400//10,stretch='No')
    # tree.update()
    # for i in range(len(keys)):
    #     tree.column(keys[i], width=75)
    
    for i in range(len(clms)):
        tup=[]
        for j in range(len(keys)):
            tup.append(getattr(clms[i],keys[j]))
        tree.insert('',END,values=tuple(tup))
    tree.pack()
    scrollbary.config(command=tree.yview)
    scrollbarx.config(command=tree.xview)
    return tree
root = Tk()
#to display contents
frame1 = Frame(root)
frame1.pack()
tree = tree_view_frame(keys,clms,frame1)
#entry table
insert_frame = Frame(root)
#insert_frame.grid(row=11,column=0,sticky='nsew')
insert_frame.pack(fill=BOTH,expand=1)
mycanvas = Canvas(insert_frame)
mycanvas.pack(side=LEFT,fill=BOTH,expand=1)
myscrollbar = Scrollbar(insert_frame,orient=VERTICAL,command=mycanvas.yview)
myscrollbar.pack(side=RIGHT,fill=Y)
mycanvas.configure(yscrollcommand=myscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

frame2= Frame(mycanvas)
mycanvas.create_window((0,0),window=frame2,anchor='nw')
# frame2 = Listbox(insert_frame)
# frame2.pack()
i,box_names=1,[]
#search box

search_box = Label(frame2,text='Search using ID',padx=20,pady=5,bg='#ffffff')
search_entry = Entry(frame2,text='ID Number')
search_box.grid(row=0,column=0)
search_entry.grid(row=0,column=1)
search_button = Button(frame2,command=search,text='Search')
search_button.grid(row=0,column=3)
for colums in keys:
    colums = Label(frame2,text=colums,padx=20,pady=5,bg='#ffffff')
    colums.grid(row=i,column=0,sticky='E')
    entry_name = Entry(frame2)
    box_names.append(entry_name) 
    entry_name.grid(row=i,column=1,padx=20)
    i+=1
#button
save = Button(frame2,text='Save',command=save)
save.grid(row=3,column=i,sticky='ns')
clear = Button(frame2,text='Clear',command=clear)
clear.grid(row=4,column=i,sticky='ns')

#search result box
search_frame = Frame(root)
search_frame.pack()

my_tree = tree_view_frame(keys,[],search_frame)

root.title('Data Processing')
root.geometry('1250x1250')
root.configure(background="#ffffff")

root.mainloop()
