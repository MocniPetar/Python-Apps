from calcualtion_of_input import calculate
import tkinter as tk
from tkinter import *
from tkinter import ttk


class calcualtor(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("Calculator")
        self.geometry("260x255")
        self.resizable(0, 0)

        self.canvas_ = Canvas(self, highlightthickness=2, bd=2, height=300, width=500)
        self.canvas_.pack()

        def set_text(text):
            self.inp.insert(END, text)
            return

        def restart_calc():
            self.inp.delete(0, END)
            return

        self.inp = StringVar()

        self.inp = Entry(self, textvariable=self.inp)
        self.inp.config(font=('Arial 35'), justify=RIGHT, width=11, highlightthickness=0, border=0)
        self.inp.place(x=26, y=15)

        one = self.Button = Button(self, width=1, border=0, text="1", command=lambda: set_text("1"))
        two = self.Button = Button(self, width=1, border=0, text="2", command=lambda: set_text("2"))
        three = self.Button = Button(self, width=1, border=0, text="3", command=lambda: set_text("3"))
        four = self.Button = Button(self, width=1, border=0, text="4", command=lambda: set_text("4"))
        five = self.Button = Button(self, width=1, border=0, text="5", command=lambda: set_text("5"))
        six = self.Button = Button(self, width=1, border=0, text="6", command=lambda: set_text("6"))
        seven = self.Button = Button(self, width=1, border=0, text="7", command=lambda: set_text("7"))
        eight = self.Button = Button(self, width=1, border=0, text="8", command=lambda: set_text("8"))
        nine = self.Button = Button(self, width=1, border=0, text="9", command=lambda: set_text("9"))
        zero = self.Button = Button(self, width=1, border=0, text="0", command=lambda: set_text("0"))
        decimal_point = self.Button = Button(self, width=1, border=0, text=".", command=lambda: set_text("."))

        addition = self.Button = Button(self, border=0, text="+", command=lambda: operators("+"))
        subtraction = self.Button = Button(self, border=0, text="-", command=lambda: operators("-"))
        mulitplication = self.Button = Button(self, border=0, text="*", command=lambda: operators("*"))
        division = self.Button = Button(self, border=0, text="/", command=lambda: operators("/"))
        equals = self.Button = Button(self, border=0, text="=", command=lambda: calculation(self))
        open_parentheses = self.Button = Button(self, border=0, text="(", command=lambda: parentheses("("))
        closed_parentheses = self.Button = Button(self, border=0, text=")", command=lambda: parentheses(")"))
        AC = self.Button = Button(self, border=0, text="AC", command=lambda: restart_calc())
        Delete = self.Button = Button(self, border=0, text="DEL", command=lambda: del_text())

        one.place(x=10, y=80)
        two.place(x=52, y=80)
        three.place(x=94, y=80)
        four.place(x=10, y=120)
        five.place(x=52, y=120)
        six.place(x=94, y=120)
        seven.place(x=10, y=160)
        eight.place(x=52, y=160)
        nine.place(x=94, y=160)
        zero.place(x=10, y=200)
        decimal_point.place(x=52, y=200)

        Delete.place(x=140, y=80)
        AC.place(x=200, y=80)
        addition.place(x=140, y=120)
        subtraction.place(x=185, y=120)
        mulitplication.place(x=140, y=160)
        division.place(x=183, y=160)
        equals.place(x=94, y=200)
        open_parentheses.place(x=140, y=200)
        closed_parentheses.place(x=183, y=200)

        def del_text():
            self.inp.delete((len(self.inp.get()) - 1))
            return

        def operators(string_):
            self.inp.insert(END, string_)
            return

        def parentheses(string_):
            self.inp.insert(END, string_)

        def input_result(result_):
            restart_calc()
            self.inp.insert(END, result_)
            return

        self.inp.focus()

        def calculation(self):
            try:
                input_ = self.inp.get()
                result = calculate.Main_Function(input_)
                input_result(result)
            except ValueError:
                pass

        # An error appears when using these two lines of code
        # self.bind(calculation(self))    
        # self.bind("<Return>", calculation(self))


if __name__ == "__main__":
    app = calcualtor()
    app.mainloop()
