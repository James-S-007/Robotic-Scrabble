import tkinter as tk

class FullScreenApp(object):
    def __init__(self, master, button_endturn_cb, button_endgame_cb):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom) 

        master.config(bg='#003057')
        # Specify Grid
        tk.Grid.rowconfigure(root,0,weight=1)
        tk.Grid.columnconfigure(root,0,weight=1)

        #Grid.rowconfigure(root,1,weight=1)
        tk.Grid.columnconfigure(root,1,weight=1)

        tk.Grid.columnconfigure(root,2,weight=1)

        endturn_button = tk.Button(text="End Turn", state=tk.NORMAL, font=('Courier', '20', 'bold'), bg = '#B3A369',command = button_endturn_cb)  
        endturn_button.grid(row=0,column=0,sticky="NSEW", padx=(20, 20), pady=(20, 20))      

        endgame_button = tk.Button(text="End Game", state=tk.NORMAL, font= ('Courier', '20', 'bold'), bg = '#B3A369', command = button_endgame_cb)
        endgame_button.grid(row=0, column=2, sticky="NSEW", padx=(20,20), pady=(20,20))  

        title = tk.Label(root, text = "Robotic Scrabble")
        title.config(font =("Courier", 28, 'bold'), bg='#003057', fg = 'white')
        title.grid(row=0, column=1, sticky="NSEW", padx=(5,5), pady=(5,5))

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

if __name__ == '__main__':
    root=tk.Tk()
    app=FullScreenApp(root, endturn_button, endgame_button)
    root.mainloop()
