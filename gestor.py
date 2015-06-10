#! -*- coding: utf-8
__author__ = 'Francisco'
import os
import sqlite3
from Tkinter import *
import Tkinter as tk

from ttk import *

from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel


mydb_path = 'database/data.db'

con = sqlite3.connect(mydb_path)
cursor = con.cursor()

if not os.path.exists(mydb_path):

    cursor.execute('''create table passwords
    (id integer primary key, name text, value text)''')





class Passwd(object):

    def __init__(self, name='',value=''):
        """Devuelve una contraseña"""
        self.name = name
        self.value = value



    def leer(self):
        try:
            cur = con.cursor()
            cur.execute("SELECT id, name, value FROM passwords")

            rows = cur.fetchall()
        except sqlite3.Error, e:
            print "Error %s;" %e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

        return rows

    def insertar(self, n, v):

        try:
            cursor.execute('''INSERT INTO passwords (name, value) VALUES (?,?)''', (n.get(), v.get()))
            con.commit()

        except Exception as e:
            # Roll back any change if something goes wrong
            con.rollback()
            print "Error %s;" %e.args[0]

            sys.exit(1)

        finally:
            if con:
                con.close()



class Vista(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.pack()
        self.create_widgets()
        self.passwd = Passwd(self)

    def v_leer(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.pack()
        self.widgets_leer()
        self.passwd = Passwd(self)



    def widgets_leer(self):
        self.title_nombre = Label(self, text="Ver contraseñas:")
        self.title_nombre.grid(row = 1, column = 1, sticky = W, pady=(10, 0))
        self.result = Label(self, text="Esto es una prueba no más.")
        self.result.grid(row = 2, column = 1, sticky = W, pady=(10,0))


    def new_window(self):
            self.newWindow = tk.Toplevel(self.master)
            self.newWindow.title("Administrador de contraseñas")
            self.newWindow.geometry("250x150")
            self.center(self.newWindow)
            self.v_leer(self.newWindow)



    def create_widgets(self):
        self.title_nombre = Label(self, text="Nombre:")
        self.title_nombre.grid(row = 1, column = 1, sticky = W, pady=(10, 0))
        nom = StringVar()
        pas = StringVar()
        self.nombre = Entry(self, textvariable=nom)
        self.nombre.grid(row = 1, column = 2, sticky = W, pady=(10, 0))
        self.title_passwd = Label(self,text="Password:")
        self.title_passwd.grid(row = 2, column = 1, sticky = W)
        self.passwd = Entry(self, textvariable= pas)
        self.passwd.grid(row = 2, column = 2, sticky = W)
        self.boton = Button(text="Añadir", command=lambda: self.passwd.insertar(nom, pas))
        self.boton.grid(columnspan=1, row=3, sticky = W, pady=(10,0), padx=(5,0))
        self.btnLeer = Button(text="Ver contraseñas", command=lambda: self.new_window())
        self.btnLeer.grid(columnspan=1, row=4, sticky = W, pady=(10,0), padx=(5,0))

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
        toplevel.deiconify()


root = Tk()
root.title("Contraseña")
root.geometry("250x150")

root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
app = Vista(root)
app.grid(column=0, row=0)
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

root.mainloop()





