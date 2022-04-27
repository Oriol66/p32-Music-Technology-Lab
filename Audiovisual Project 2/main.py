    # This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import Repreductor

import playsound
import os
import tkinter as tk


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script. LALALALALALA
if __name__ == '__main__':
    print_hi('Projecte audiovisual')

    window = tk.Tk()
    window.title("Finestra main")
    window.geometry('800x600') #tamany de la finestra
    window.configure(background='black') #Color de fons (no posar espais al costat del '=')

    label1 = tk.Label(window, text="Reproductor P32", bg='red', fg='white') #(actua a la finestra, escriu reproductor P32, bg=color de fons de lletra vermell, fg=color de lletra blanc
    label1.pack()

    label2 = tk.Label(window, text="Patates", bg='yellow', fg='white')
    label2.pack(fill=tk.X) #omplim el fons horitzontalment

    label3 = tk.Label(window, text="calçots", bg='yellow', fg='white')
    label3.pack(padx=20, pady=50, ipadx=15, ipady=40) #deixa 20 horitzontal i 50 vertical, cobreix el fons amb 15H i 40V

    label4 = tk.Label(window, text="Ceba", bg='orange', fg='white')
    label4.pack(side=tk.LEFT) #deixa 20 a l'esqurra i 50 a la dreta

    finish = Repreductor.main_reproductor()



    #window.mainloop()



    #playsound.playsound('Demo3.mp3')#Ha d'estar en la carpeta del programa

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
