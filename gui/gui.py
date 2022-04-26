from tkinter import *

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom) 

        # Specify Grid
        Grid.rowconfigure(root,0,weight=1)
        Grid.columnconfigure(root,0,weight=1)

        Grid.rowconfigure(root,1,weight=1)
        Grid.columnconfigure(root,1,weight=1)

        endButton = Button(text="End Turn", state=NORMAL, font=('Helvetica', '20'))  
        endButton.grid(row=0,column=1,sticky="NSEW", padx=(20, 20), pady=(20, 20))        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

root=Tk()
app=FullScreenApp(root)

root.mainloop()
