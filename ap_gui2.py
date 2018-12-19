

import os
import tkinter
from tkinter import ttk


import matplotlib
matplotlib.use("TkAgg")


class ApGui :
    INITIAL_SIZE = '500x400'
    # INITIAL_SIZE = '450x600'
    # INITIAL_SIZE = '450x600'
    def __init__(self,path) :
        self.set_up_gui()
        self.root_path = path

        # tree.bind('<<TreeviewOpen>>', update_tree)
        # tree.bind('<Double-Button-1>', change_dir)

        self.tree.heading("#0", text="", anchor='w')

        self.tree.column("type", stretch=0, width=100)


        self.pop_root(path)
        self.root.mainloop()


    def set_up_gui(self) :
        self.root = tkinter.Tk()

        self.vsb = ttk.Scrollbar(orient="vertical")     # vsb -> vertical_scroll_bar
        self.hsb = ttk.Scrollbar(orient="horizontal")   # hsb -> horizontal_scroll_bar


        # tree = ttk.Treeview(columns=("fullpath", "type", "size"),
        #     displaycolumns="size", yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
        #     xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

        self.tree = ttk.Treeview(columns=("type"),yscrollcommand=lambda f, l: ApGui.autoscroll(self.vsb, f, l),
            xscrollcommand=lambda f, l:ApGui.autoscroll(self.hsb, f, l))

        self.vsb['command'] = self.tree.yview
        self.hsb['command'] = self.tree.xview

        self.tree.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.geometry(ApGui.INITIAL_SIZE)

    def pop_root(self, path) :


        node_name = os.path.basename(path)
        self.root_node = self.tree.insert('', 'end', text=node_name, values=['d'],open=True)


        # rh30_runs = []
        with os.scandir(path) as it :
            for entry in it :
                if entry.is_dir() and entry.name.startswith('20') :
                    #rh30_runs.append(entry.name)
                    temp = self.tree.insert(self.root_node,'end', text=entry.name, values=['d'],open=True)
                    self.pop_with_contents(temp)


    def pop_with_contents(self, node) :
        # print(self.tree.item(node, 'text'))
        node_path = os.path.join(self.root_path, self.tree.item(node, 'text'))
        with os.scandir(node_path) as it :
            for entry in it :
                # if entry.is_dir() :
                #     self.tree.insert(node,'end',text=entry.name,values=['d'],open=True)


                if entry.is_dir() : type = 'd'
                else : type = 'f'
                
                self.tree.insert(node,'end',text=entry.name,values=[type],open=True)


    @staticmethod
    def autoscroll(sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)


root_path = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)'

rh30_root_path = os.path.join(root_path, 'RH30')

butt = ApGui(rh30_root_path)
