#! -*- coding: utf-8
__author__ = 'Francisco Fuentes'
import os
import sqlite3
from Tkinter import *
import Tkinter as tk
from ttk import *

mydb_path = 'database/data.db'

if not os.path.exists(mydb_path):
    os.makedirs('database')
    con = sqlite3.connect(mydb_path)
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE passwords
    (id INTEGER PRIMARY KEY, name TEXT, value TEXT)''')


class Passwd():
    """Controls database transactions to save and read passwords"""
    def leer(self):
        """
        :return: an array of passwords with names and identifiers.
        """
        try:
            con = sqlite3.connect(mydb_path)
            cur = con.cursor()
            cur.execute("SELECT id, name, value FROM passwords")

            rows = cur.fetchall()
        except sqlite3.Error, e:
            print "Error %s;" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

        return rows

    def insertar(self, n, v):
        """
        Adds a new password to the database
        :param n: string (descriptive name of a password)
        :param v: string (the password itself)
        :return: void
        """
        try:
            con = sqlite3.connect(mydb_path)
            cursor = con.cursor()
            cursor.execute('''INSERT INTO passwords (name, value) VALUES (?,?)''', (n.get(), v.get()))
            con.commit()

        except Exception as e:
            # Roll back any change if something goes wrong
            con.rollback()
            print "Error %s;" % e.args[0]

            sys.exit(1)

        finally:
            if con:
                con.close()

    def deletepass(self, item):
        """
        Deletes a row from passwords
        :param item: List (list with name and password)
        :return: void
        """
        name = item[1]
        value = item[2]

        try:
            con = sqlite3.connect(mydb_path)
            cursor = con.cursor()
            cursor.execute('''DELETE FROM passwords WHERE name = ? AND value = ?''', (name, value))
            con.commit()

        except Exception as e:
            # Rolls back any changes if something goes wrong
            con.rollback()
            print "Error %s;" % e.args[0]

            sys.exit(1)

        finally:
            if con:
                con.close()


class Vista(Frame):
    """
    Displays all windows.
    """
    def __init__(self, master):
        """

        :param master: Main Window
        :return: TK object
        """
        Frame.__init__(self, master)
        self.grid()
        self.pack()
        self.create_widgets()
        self.passwd = Passwd()

    def v_leer(self, master):
        """

        :param master: Main Window
        :return: Displays a child window.
        """
        Frame.__init__(self, master)
        self.grid()
        self.pack()
        self.widgets_leer()
        self.passwd = Passwd()
        try:
            self.Lb1.bind('<Button-3>', self.__copyToClipboard)
            print("Data copied to the clipboard")
        except TclError:
            print("Error copying data to the clipboard")

    def widgets_leer(self):
        """

        :return: Displays widgets inside the child window "leer"
        """
        self.title_nombre = Label(self, text="See passwords:")
        self.title_nombre.grid(row=1, column=1, sticky=W, pady=(10, 0))
        self.result = Label(self, text="Right click to copy")
        self.result.grid(row=2, column=1, sticky=W, pady=(10, 0))
        self.btnBorrar = Button(self, text="Delete", command=lambda: self.passwd.deletepass(self.__selectpassword()))
        self.btnBorrar.grid(row=10, column=1, sticky=W, pady=(10, 0))
        self.passwords = Passwd().leer()
        self.Lb1 = Listbox(self)
        y = 0
        for x in self.passwords:
            if x[1]:
                self.Lb1.insert(y, x)
                y += 1
        self.Lb1.grid(row=3, column=1, sticky=W, pady=(10, 0))

    def __copyToClipboard(self, event):
        """
        Sends the content of a listbox row to the users clipboard.
        :param event: Right click
        :return: void.
        """
        self.clipboard_clear()
        self.lista = self.Lb1.get(self.Lb1.curselection())[2]
        print self.lista
        self.clipboard_append(self.lista)

    def __selectpassword(self):
        """
        Deletes a password from the table
        :param event:
        :return: void.
        """

        self.item = self.Lb1.get(self.Lb1.curselection())
        return self.item

    def new_window(self):
        """
        Draws the child window and sets its behavior.
        :return:
        """
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Password Manager")
        self.newWindow.geometry("250x400")
        self.center(self.newWindow)
        self.v_leer(self.newWindow)
        self.newWindow.protocol("WM_DELETE_WINDOW", self.newWindow.withdraw)

    def create_widgets(self):
        """
        Creates the main window widgets.
        :return:
        """
        self.title_nombre = Label(self, text="Name:")
        self.title_nombre.grid(row=1, column=1, sticky=W, pady=(10, 0))
        nom = StringVar()
        pas = StringVar()
        self.nombre = Entry(self, textvariable=nom)
        self.nombre.grid(row=1, column=2, sticky=W, pady=(10, 0))
        self.title_passwd = Label(self, text="Password:")
        self.title_passwd.grid(row=2, column=1, sticky=W)
        self.passwd = Entry(self, textvariable=pas)
        self.passwd.grid(row=2, column=2, sticky=W)
        self.boton = Button(text="Add", command=lambda: self.passwd.insertar(nom, pas))
        self.boton.grid(columnspan=1, row=3, sticky=W, pady=(10, 0), padx=(5, 0))
        self.btnLeer = Button(text="See passwords", command=lambda: self.new_window())
        self.btnLeer.grid(columnspan=1, row=4, sticky=W, pady=(10, 0), padx=(5, 0))

    def center(self, toplevel):
        """
        Necessary to put the child window in the middle of the screen
        :param toplevel: Main Window
        :return:
        """
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def main():
            """
        Starts the application
        :return:
        """
    root = Tk()
    root.title("Password")
    root.geometry("250x150")

    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    app = Vista(root)
    app.grid(column=0, row=0)
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    root.mainloop()

if __name__ == '__main__':
    main()