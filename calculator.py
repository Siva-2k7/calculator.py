import tkinter as tk
from tkinter import font
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Generated Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Custom fonts
        self.display_font = font.Font(family="Arial", size=32, weight="bold")
        self.button_font = font.Font(family="Arial", size=18)
        self.small_button_font = font.Font(family="Arial", size=14)
        
        # Calculator variables
        self.current_input = "0"
        self.stored_value = None
        self.current_operation = None
        self.should_reset_input = False
        self.last_operation = None
        
        # Create UI elements
        self.create_display()
        self.create_buttons()
        
        # Add key bindings
        self.root.bind("<Key>", self.handle_key_press)
        
    def create_display(self):
        # Main display frame
        display_frame = tk.Frame(self.root, bg="#34495e", height=150, 
                                 padx=20, pady=20, bd=0, highlightthickness=0)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Display label
        self.display_var = tk.StringVar(value="0")
        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            anchor=tk.E, 
            bg="#34495e", 
            fg="#ecf0f1",
            font=self.display_font,
            padx=10
        )
        display_label.pack(expand=True, fill=tk.BOTH)
        
        # Memory indicator
        self.memory_var = tk.StringVar()
        memory_label = tk.Label(
            display_frame, 
            textvariable=self.memory_var, 
            anchor=tk.E, 
            bg="#34495e", 
            fg="#7f8c8d",
            font=self.small_button_font
        )
        memory_label.pack(fill=tk.X)
        
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Button grid configuration
        button_grid = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '='],
            ['π', 'e', '√', 'x²'],
            ['%', 'sin', 'cos', 'tan']
        ]
        
        # Create buttons
        for row_idx, row in enumerate(button_grid):
            button_frame.rowconfigure(row_idx, weight=1)
            for col_idx, btn_text in enumerate(row):
                button_frame.columnconfigure(col_idx, weight=1)
                
                # Button styling
                bg_color = "#34495e"
                fg_color = "#ecf0f1"
                active_bg = "#3d566e"
                font = self.button_font  # Always set default font first

                # Special styling for operation buttons
                if btn_text in {'÷', '×', '-', '+', '='}:
                    bg_color = "#3498db"
                    active_bg = "#2980b9"
                elif btn_text in {'C', 'CE', '⌫'}:
                    bg_color = "#e74c3c"
                    active_bg = "#c0392b"
                elif btn_text in {'π', 'e', '√', 'x²', '%', 'sin', 'cos', 'tan'}:
                    bg_color = "#2ecc71"
                    active_bg = "#27ae60"
                    font = self.small_button_font  # Override font for these buttons

                btn = tk.Button(
                    button_frame, 
                    text=btn_text,
                    command=lambda t=btn_text: self.on_button_click(t),
                    font=font,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground=active_bg,
                    activeforeground=fg_color,
                    relief=tk.FLAT,
                    bd=0,
                    padx=0,
                    pady=0,
                    highlightthickness=0
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)
    
    def on_button_click(self, button_text):
        # Handle different button types
        if button_text.isdigit():
            self.add_digit(button_text)
        elif button_text == '.':
            self.add_decimal()
        elif button_text in {'+', '-', '×', '÷'}:
            self.set_operation(button_text)
        elif button_text == '=':
            self.calculate_result()
        elif button_text == 'C':
            self.clear_all()
        elif button_text == 'CE':
            self.clear_entry()
        elif button_text == '⌫':
            self.backspace()
        elif button_text == '±':
            self.toggle_sign()
        elif button_text == '√':
            self.calculate_square_root()
        elif button_text == 'x²':
            self.calculate_square()
        elif button_text == 'π':
            self.add_pi()
        elif button_text == 'e':
            self.add_e()
        elif button_text == '%':
            self.calculate_percentage()
        elif button_text in {'sin', 'cos', 'tan'}:
            self.calculate_trig(button_text)
    
    def add_digit(self, digit):
        if self.should_reset_input or self.current_input == "0":
            self.current_input = digit
            self.should_reset_input = False
        else:
            self.current_input += digit
        self.update_display()
    
    def add_decimal(self):
        if '.' not in self.current_input:
            self.current_input += '.'
            self.update_display()
    
    def set_operation(self, operation):
        if self.current_operation and not self.should_reset_input:
            self.calculate_result()
        
        self.stored_value = self.current_input
        self.current_operation = operation
        self.should_reset_input = True
        self.memory_var.set(f"{self.stored_value} {self.get_operation_symbol()}")
    
    def calculate_result(self):
        if not self.current_operation or not self.stored_value:
            return
            
        try:
            operand1 = float(self.stored_value)
            operand2 = float(self.current_input)
            
            if self.current_operation == '+':
                result = operand1 + operand2
            elif self.current_operation == '-':
                result = operand1 - operand2
            elif self.current_operation == '×':
                result = operand1 * operand2
            elif self.current_operation == '÷':
                if operand2 == 0:
                    raise ZeroDivisionError
                result = operand1 / operand2
            
            # Format result
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
            
            self.last_operation = self.current_operation
            self.current_operation = None
            self.stored_value = None
            self.should_reset_input = True
            self.memory_var.set("")
            self.update_display()
            
        except ZeroDivisionError:
            self.display_error("Cannot divide by zero")
        except Exception:
            self.display_error("Error")
    
    def clear_all(self):
        self.current_input = "0"
        self.stored_value = None
        self.current_operation = None
        self.should_reset_input = False
        self.memory_var.set("")
        self.update_display()
    
    def clear_entry(self):
        self.current_input = "0"
        self.update_display()
    
    def backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()
    
    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def calculate_square_root(self):
        try:
            value = float(self.current_input)
            if value < 0:
                raise ValueError
            result = math.sqrt(value)
            self.format_and_set_result(result)
        except ValueError:
            self.display_error("Invalid input")
    
    def calculate_square(self):
        try:
            value = float(self.current_input)
            result = value ** 2
            self.format_and_set_result(result)
        except Exception:
            self.display_error("Error")
    
    def add_pi(self):
        self.current_input = str(math.pi)
        self.should_reset_input = True
        self.update_display()
    
    def add_e(self):
        self.current_input = str(math.e)
        self.should_reset_input = True
        self.update_display()
    
    def calculate_percentage(self):
        try:
            value = float(self.current_input)
            result = value / 100
            self.format_and_set_result(result)
        except Exception:
            self.display_error("Error")
    
    def calculate_trig(self, func):
        try:
            value = float(self.current_input)
            angle_rad = math.radians(value)
            
            if func == 'sin':
                result = math.sin(angle_rad)
            elif func == 'cos':
                result = math.cos(angle_rad)
            elif func == 'tan':
                result = math.tan(angle_rad)
                
            self.format_and_set_result(result)
        except Exception:
            self.display_error("Error")
    
    def format_and_set_result(self, result):
        # Format result to avoid long decimal tails
        if abs(result) < 1e10 and abs(result) > 1e-10 or result == 0:
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
        else:
            self.current_input = "{:.6e}".format(result)
            
        self.should_reset_input = True
        self.update_display()
    
    def display_error(self, message):
        self.current_input = message
        self.should_reset_input = True
        self.update_display()
        self.memory_var.set("")
        self.root.after(2000, self.clear_entry)
    
    def update_display(self):
        # Format large numbers for display
        if len(self.current_input) > 12:
            try:
                num = float(self.current_input)
                self.display_var.set("{:.6e}".format(num))
            except:
                self.display_var.set(self.current_input[:12] + "...")
        else:
            self.display_var.set(self.current_input)
    
    def get_operation_symbol(self):
        symbols = {
            '+': '+',
            '-': '-',
            '×': '×',
            '÷': '÷'
        }
        return symbols.get(self.current_operation, '')
    
    def handle_key_press(self, event):
        key = event.char
        keys_map = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '.': '.', '+': '+', '-': '-', '*': '×', '/': '÷',
            '=': '=', '\r': '=', '\x08': '⌫', '\x1b': 'C'
        }
        
        if key in keys_map:
            self.on_button_click(keys_map[key])

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()