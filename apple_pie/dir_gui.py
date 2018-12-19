"""A directory browser using Ttk Treeview.

Based on the demo found in Tk 8.5 library/demos/browse
"""
import os
import glob
import tkinter
from tkinter import ttk
from hurry.filesize import size as fsize

def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    parent = tree.parent(node)
    special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

    for p in os.listdir(path):
    # for p in special_dirs + os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        if os.path.isdir(p): ptype = "directory"
        elif os.path.isfile(p): ptype = "file"

        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text=fname, values=[p, ptype])

        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text="dummy")
                tree.item(id, text=fname)
        elif ptype == 'file':
            size_in_bytes = os.stat(p).st_size
            tree.set(id, "size", "{}B".format(fsize(size_in_bytes)))


def populate_roots(tree,dir):
    #dir = os.path.abspath('.').replace('\\', '/')
    #dir_txt = dir.replace(' ','\s')
    node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
    populate_tree(tree, node)

def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())

def change_dir(event):
    tree = event.widget
    node = tree.focus()
    if tree.parent(node):
        path = os.path.abspath(tree.set(node, "fullpath"))
        if os.path.isdir(path):
            os.chdir(path)
            tree.delete(tree.get_children(''))
            populate_roots(tree,node)

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

def dir_gui(dir) :
    root = tkinter.Tk()

    vsb = ttk.Scrollbar(orient="vertical")
    hsb = ttk.Scrollbar(orient="horizontal")

    tree = ttk.Treeview(columns=("fullpath", "type", "size"),
        displaycolumns="size", yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
        xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

    vsb['command'] = tree.yview
    hsb['command'] = tree.xview

    tree.heading("#0", text="Directory Structure", anchor='w')
    tree.heading("size", text="File Size", anchor='w')
    #tree.column("#0", stretch=1, width=350)
    tree.column("size", stretch=0, width=100)

    populate_roots(tree,dir)
    tree.bind('<<TreeviewOpen>>', update_tree)
    tree.bind('<Double-Button-1>', change_dir)

    # Arrange the tree and its scrollbars in the toplevel
    tree.grid(column=0, row=0, sticky='nswe')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.geometry('450x600')
    # print(type(root))
    root.mainloop()
    # return root


#
# root_path = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'
#
# ## /RH30/20181106'
#
#
# rh30_root_path = os.path.join(root_path, 'RH30')
#
#
# root =  run_gui(root_path)
