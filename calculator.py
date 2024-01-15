from tkinter import *

def button_click(char):
    current = text_input.get()
    text_input.delete(0, END)
    text_input.insert(END, current + str(char))

def button_clear_all():
    text_input.delete(0, END)

def button_delete():
    current = text_input.get()[:-1]
    text_input.delete(0, END)
    text_input.insert(END, current)

def button_equal():
    try:
        result = str(eval(text_input.get()))
        text_input.delete(0, END)
        text_input.insert(END, result)
    except Exception as e:
        text_input.delete(0, END)
        text_input.insert(END, "Error")

tk_calc = Tk()
tk_calc.configure(bg="#293C4A", bd=10)
tk_calc.title("Simple Calculator")

text_input = Entry(tk_calc, font=('sans-serif', 20, 'bold'),
                   bd=5, insertwidth=5, bg='#BBB', justify='right')
text_input.grid(columnspan=4, padx=10, pady=15)

button_params = {'bd': 5, 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 20, 'bold')}
button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 20, 'bold')}

for i in range(10):
    Button(tk_calc, button_params_main, text=str(i),
           command=lambda i=i: button_click(i)).grid(row=(i // 3) + 1, column=(i % 3), sticky="nsew")

operators = ['+', '-', '*', '/']
for i, operator in enumerate(operators):
    Button(tk_calc, button_params_main, text=operator,
           command=lambda operator=operator: button_click(operator)).grid(row=i + 1, column=3, sticky="nsew")

Button(tk_calc, button_params_main, text='.',
       command=lambda: button_click('.')).grid(row=4, column=0, sticky="nsew")
Button(tk_calc, button_params_main, text='0',
       command=lambda: button_click('0')).grid(row=4, column=1, sticky="nsew")
Button(tk_calc, button_params_main, text='=',
       command=button_equal).grid(row=4, column=2, columnspan=2, sticky="nsew")

Button(tk_calc, button_params_main, text='C',
       command=button_clear_all, bg='#db701f').grid(row=1, column=4, sticky="nsew")
Button(tk_calc, button_params_main, text='DEL',
       command=button_delete, bg='#db701f').grid(row=2, column=4, sticky="nsew")

tk_calc.mainloop()
