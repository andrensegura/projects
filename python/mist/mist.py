import tkinter as tk
import os, subprocess, json

#config file that holds all the game names/paths
games = json.loads(open(".\games.json").read())

class Application(tk.Frame):
    #ok this shit bugs me. this used to be a variable inside createWidgets.
    #I moved it out so that it could be accessed elsewhere and I could
    #destroy the widgets when needed. But I moved it out, made no further
    #changes, and the buttons get overwritten anyway. wtf?
    buttons = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):

        #MENU
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        file = tk.Menu(menubar)
        file.add_command(label="Add Game", command=lambda: self.browse())
        menubar.add_cascade(label="File", menu=file)
    
        #BUTTONS
        for i in range(len(games)):
            name = games[str(i)]["name"]
            path = games[str(i)]["path"]
            self.buttons.append(tk.Button(self, width = 20 ))
            self.buttons[i]["text"] = name
            self.buttons[i]["command"] = lambda path=path: \
                                         subprocess.Popen(path, close_fds=True, \
                                         stdin=None, stdout=None, stderr=None)
            self.buttons[i].pack(side="top")
            
    def add_game():
        pass
            
    def browse(self):
        from tkinter.filedialog import askopenfilename
        self.filepath = askopenfilename()
        self.filename = os.path.basename(self.filepath)
        if os.path.isfile(self.filepath):
            self.filenameText = os.path.splitext(self.filename)[0]
            self.filenameExt = os.path.splitext(self.filename)[1]
            if self.filenameExt == ".exe":
                games[str(len(games))] = {"name": self.filenameText, "path": self.filepath}
                with open(".\games.json", 'w') as out:
                    out.write(json.dumps(games, sort_keys=True, indent=4, separators=(',', ': ')))
                self.createWidgets()
            else:
                #handle the file not being an exe
                print("Not an executable file!")
        else:
            #somethings fucked up
            pass

root = tk.Tk()
app = Application(master=root)
app.mainloop()
