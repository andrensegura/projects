import Tkinter as tk
import socket
import thread
from settings import *
from pyglet import media


def connectToServer(textField, user, host, port):
    s = socket.socket()
    port = int(port)

    try:
        s.connect((host, port))
        s.send(user)
        textField.configure(state = tk.NORMAL)
        textField.insert(tk.END, 'CONNECTED TO SERVER.')
        media.load(loginChime).play()
        textField.configure(state = tk.DISABLED)
    except:
        textField.configure(state = tk.NORMAL)
        textField.insert(tk.END, '\r\nSERVER NOT RESPONDING.')
        textField.configure(state = tk.DISABLED)
        return

    return s

def getMessages(server, textField):
    while True:
        try:
            servMess = server.recv(1024)
            textField.configure(state = tk.NORMAL)
            textField.insert(tk.END, "\r\n" + servMess)
            textField.configure(state = tk.DISABLED)
            textField.yview(tk.END)
            media.load(msgChime).play()
        except:
            return

def sendMessage(server, user, textField, window):
    message = textField.get()
    textField.delete(0, 'end')
    if message == '':
        return
    elif message == '/logout':
        server.send(message)
        server.close
        media.load(logoutChime).play()
        window.destroy()
    elif message[0] == '/':
        server.send(message)
    else:
        server.send(message)



class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.configure(background=frameBackgroundColor)

        #username box
        tk.Label(self, text="Username", background=frameBackgroundColor).grid(row = 0, column = 0)
        userBox = tk.Entry(self)
        userBox.focus()
        userBox.grid(row=0, column=1)

        #hostname box
        tk.Label(self, text="Hostname", background=frameBackgroundColor).grid(row = 1, column = 0)
        hostBox = tk.Entry(self)
        hostBox.grid(row=1, column=1)

        #port box
        tk.Label(self, text="Port #", background=frameBackgroundColor).grid(row=2, column = 0)
        portBox = tk.Entry(self)
        portBox.grid(row=2, column=1)

        #interesting thing here. The "_:" is necessary
        # http://stackoverflow.com/questions/16215045/typeerror-lambda-takes-no-arguments-1-given
        userBox.bind('<Return>', lambda _: self.create_window(userBox.get(), hostBox.get(), portBox.get()) )
        hostBox.bind('<Return>', lambda _: self.create_window(userBox.get(), hostBox.get(), portBox.get()) )
        portBox.bind('<Return>', lambda _: self.create_window(userBox.get(), hostBox.get(), portBox.get()) )

        #connect button
        self.connButton = tk.Button(self, text="Connect", background=buttonColor,
                            command = lambda: self.create_window(userBox.get(), hostBox.get(), portBox.get()))
        self.connButton.grid(row=3)


    def create_window(self, user, host, port):
        if not user or not host or not port:
            return

        t = tk.Toplevel(self)
        t.wm_title("%s:%s" % (host, port))
        t.configure(background = frameBackgroundColor)
        t.wm_iconbitmap(faviconImage)
        t.geometry("400x500")


        t.columnconfigure(0, weight=1)
        t.rowconfigure(0, weight=1)

        #server input
        textBox = tk.Text(t)
        textBox.grid(row = 0 , column = 0 , columnspan=2, padx=3, pady=3, sticky = "news")
		
        #obviously a scroll bar
        #scrollBar = tk.Scrollbar(t)
        #scrollBar.grid(row = 0 , column = 1, sticky = 'nse')
        #scrollBar.grid(in_=textBox, sticky = tk.N + tk.S)

        #scrollBar.config(command = textBox.yview)
        #textBox.config(yscrollcommand = scrollBar.set , state = tk.DISABLED) #, bg = '#99CCFF')
        #^^^ DISABLED makes the text uneditable. You can't INSERT either though, so you
        #    need to change the state to NORMAL before inserting, then DISABLED when you're done.

        #user input
        messageBox = tk.Entry(t)
        messageBox.focus()
        messageBox.grid(row = 1 , column = 0 , padx=2, pady=2, sticky = tk.W + tk. E)
        messageBox.bind('<Return>', lambda _: sendMessage(server, user, messageBox, t) )



        #send button
        #sendButton = tk.Button(t, text="send", bg=buttonColor, 
        #                       command = lambda: sendMessage(server, user, messageBox, t))
        #sendButton.grid(row = 1 , column = 1, padx=2, pady=2, sticky = tk.E)

        server = connectToServer(textBox, user, host, port)
        thread.start_new_thread(getMessages, (server, textBox, ))
		



if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(faviconImage)
    #root.configure(background = 'black')
    root.title("Gurgle")
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
