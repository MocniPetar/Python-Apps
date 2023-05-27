from ctypes import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import sys
import os

clib_InfixToPostfix = cdll.LoadLibrary("/Users/pierstrbad/Desktop/Programi/Python/Finished Projects/StogAppWithCAndPython/CLibrary_InfixToPostfix.so")
clib_Postfix_Calc = cdll.LoadLibrary("/Users/pierstrbad/Desktop/Programi/Python/Finished Projects/StogAppWithCAndPython/CLibrary_Postfix_Calc.so")

clib_InfixToPostfix.PythonFunction.argtypes = [c_char_p]
clib_InfixToPostfix.PythonFunction.restype = c_char_p

clib_Postfix_Calc.PythonFunction.argtypes = [c_char_p]
clib_Postfix_Calc.PythonFunction.restype = c_float

class Stog(tk.Tk):
    def __init__(window): # Defining the class Stog initializer to "window"
        super().__init__()
        
        window.title("Racunanje postfix izraza")
        window.geometry("300x350")
        window.resizable(0,0)
        
        window.fileName = StringVar()
        window.Entry_1 = StringVar()
        window.options = [
            "Expression",
        ]
        
        # ----------FUNCTIONS----------- #
        
        # This restart funciton is not the best way beacuse the program
        # actually closes and starts again which is not User Frindly
        # Try to make the restarting seamless
        
        def check_error(error_code):
            if error_code == -2.0002:
                return "The operation or value is not correct!"
            elif error_code == -3.0003:
                return "There is more than one element left in stack!"
            elif error_code == -4.0004:
                return "Undefined!"
            else:
                return None
        
        def restart_app():
            
            clib_InfixToPostfix.free.argtypes = [c_char_p]
            clib_InfixToPostfix.free.restype = c_char_p
                
            clib_Postfix_Calc.free.argtypes = [c_char_p]
            clib_Postfix_Calc.free.restype = c_float

            python = sys.executable
            os.execl(python, python, * sys.argv)
        
        def open_file():
            filetypes = (
                ('text files', '*.txt'),
            )
            window.options.clear()
            window.DropDownMenu.delete(0,'end')
            
            window.file = fd.askopenfile(filetypes = filetypes)
            if window.file:
                window.fileName = os.path.abspath(window.file.name)
                
            with open(window.fileName) as file:
                list = [line.rstrip() for line in file]
                
            for a in list:
                window.DropDownMenu['values'] += (a,)
            
            return
        
        def print_():
            string_ = window.Entry_1.get()
            string_2 = window.SelectedExpresion.get()
            Infix = None
            Result = None
            
            if string_ != '':
                
                Infix = clib_InfixToPostfix.PythonFunction(string_.encode())
                Result = clib_Postfix_Calc.PythonFunction(Infix)
                
            elif string_2 != '':
                
                Infix = clib_InfixToPostfix.PythonFunction(string_2.encode())
                Result = clib_Postfix_Calc.PythonFunction(Infix)
            
            window.Postfix = Label(window, text = Infix)
            window.Postfix.config(font = "Arial 16")
            window.Postfix.place(x = 20, y = 250)
            
            ERROR_Mes =  check_error(round(Result,4))    
            
            if ERROR_Mes == None:
                window.Result = Label(window, text = Result)
                window.Result.config(font = "Arial 16")
                window.Result.place(x = 20, y = 315)
            else:
                window.Result = Label(window, text = ERROR_Mes)
                window.Result.config(font = "Arial 13")
                window.Result.place(x = 20, y = 315)
                
            clib_InfixToPostfix.free.argtypes = [c_char_p]
            clib_InfixToPostfix.free.restype = c_char_p

            clib_Postfix_Calc.free.argtypes = [c_char_p]
            clib_Postfix_Calc.free.restype = c_float
            
            return
        
        # --------LABEL WIDGETS--------- #
        
        window.Tekst_1 = Label(window, text = "Unesite infix izraz ili odaberite datoteku")
        window.Tekst_1.config(font = "Arial 16")
        window.Tekst_1.place(x = 5, y = 20)
        
        window.Tekst_2 = Label(window, text = "Izraz:")
        window.Tekst_2.config(font = "Arial 15")
        window.Tekst_2.place(x = 10, y = 60)
        
        window.Tekst_3 = Label(window, text = "(ODABERITE .TXT FILE U KOJEMU IMATE INFIX IZRAZ)")
        window.Tekst_3.config(font = "Arial 9")
        window.Tekst_3.place(x = 5, y = 40)
        
        window.Tekst_4 = Label(window, text = "Sadrzaj datoteke:")
        window.Tekst_4.config(font = "Arial 15")
        window.Tekst_4.place(x = 10, y = 115)
        
        window.Tekst_5 = Label(window, text = "Postfix izraz:")
        window.Tekst_5.config(font = "Arial 15")
        window.Tekst_5.place(x = 10, y = 220)
        
        window.Tekst_5 = Label(window, text = "Iznos:")
        window.Tekst_5.config(font = "Arial 15")
        window.Tekst_5.place(x = 10, y = 280)
        
        # --------ENTRY WIDGETS--------- #
        
        window.Entry_1 = Entry(window, textvariable = window.Entry_1)
        window.Entry_1.config(font =('Arial 20'), justify = LEFT, width = 15, highlightthickness = 0, border = 0)
        window.Entry_1.place(x = 10, y = 85)
        
        # --------BUTTON WIDGETS-------- #
        
        window.Button_1 = Button(window, text = "Open File", command = open_file)
        window.Button_1.place(x = 200, y = 83)
        
        window.Button_2 = Button(window, text = "Convert and calculate", command = print_)
        window.Button_2.place(x = 10, y = 180)
        
        window.Restart_Button = Button(window, text = "Restart", command = restart_app)
        window.Restart_Button.place(x = 200, y = 300)
        
        # -------COMBOBOX WIDGET-------- #
        
        window.SelectedExpresion = StringVar(window)
        window.SelectedExpresion.set(window.options[0])
        
        window.DropDownMenu = ttk.Combobox(window, textvariable = window.SelectedExpresion)
        window.DropDownMenu['values'] = window.options
        window.DropDownMenu['state'] = 'readonly'
        window.DropDownMenu.place(x = 20, y = 145)
     
if __name__ == "__main__":
    Stog().mainloop()