

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



        self.pop_root(path)
        self.root.mainloop()


    def set_up_gui(self) :
        self.root = tkinter.Tk()

        self.vsb = ttk.Scrollbar(orient="vertical")     # vsb -> vertical_scroll_bar
        self.hsb = ttk.Scrollbar(orient="horizontal")   # hsb -> horizontal_scroll_bar


        # tree = ttk.Treeview(columns=("fullpath", "type", "size"),
        #     displaycolumns="size", yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
        #     xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

        self.tree = ttk.Treeview(columns=("file_count","czi_count","csv_count"),displaycolumns=("file_count","czi_count"), yscrollcommand=lambda f, l: ApGui.autoscroll(self.vsb, f, l),
            xscrollcommand=lambda f, l:ApGui.autoscroll(self.hsb, f, l))

        self.tree.column("czi_count", stretch=0, width=100)
        self.tree.column("csv_count", stretch=0, width=100)
        self.tree.column("file_count", stretch=0, width=100)


        self.tree.heading("#0", text="Expers", anchor='w')
        self.tree.heading("czi_count", text="czi_count", anchor='w')
        self.tree.heading("csv_count", text="csv_count", anchor='w')
        self.tree.heading("file_count", text="file_count", anchor='w')
        # self.tree = ttk.Treeview(columns=("type"),yscrollcommand=lambda f, l: ApGui.autoscroll(self.vsb, f, l),
        #     xscrollcommand=lambda f, l:ApGui.autoscroll(self.hsb, f, l))

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
        self.root_node = self.tree.insert('', 'end', text=node_name, open=True)


        # rh30_runs = []
        with os.scandir(path) as it :
            for entry in it :
                if entry.is_dir() and entry.name.startswith('20') :
                    #rh30_runs.append(entry.name)
                    temp = self.tree.insert(self.root_node,'end', text=entry.name, open=True)
                    self.pop_with_contents(temp)


    def pop_with_contents(self, node) :
        czi_count = 0
        #has_csv_dir = False
        csv_count = 0

        # print(self.tree.item(node, 'text'))
        node_path = os.path.join(self.root_path, self.tree.item(node, 'text'))
        with os.scandir(node_path) as it :
            for entry in it :
                # if entry.is_dir() :
                #     self.tree.insert(node,'end',text=entry.name,values=['d'],open=True)

                if entry.is_dir() :
                    temp = self.tree.insert(node,0,text=entry.name+'/',open=True)
                    if entry.name == 'Csv' :
                        for f in os.listdir(os.path.join(node_path,entry.name)) :
                            if f.endswith('.csv') :
                                csv_count += 1
                    self.tree.set(temp, 'file_count',len(os.listdir(os.path.join(node_path,entry.name))))
                #elif 'plate-map' in entry.name :
                if entry.name.endswith('_plate-map.csv') :
                    self.tree.insert(node,'end',text=entry.name,open=True)
                elif entry.name.endswith('.czi') :
                    czi_count += 1
                #self.tree.insert(node,'end',text=str(czi_count),open=True)

        self.tree.set(node,'czi_count',czi_count)
        self.tree.set(node,'csv_count',csv_count)



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
