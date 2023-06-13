def get_sign_bit(decimal):
    if decimal < 0:
        return '1'
    else:
        return '0'

def get_exponent_bits(binary):
    if '.' in binary:
        integer_bits, fractional_bits = binary.split('.')
        if integer_bits != '0':
            exponent = len(integer_bits) - 1
        else:
            exponent = -len(fractional_bits.split('1')[0]) - 1
    else:
        exponent = len(binary) - 1

    exponent += 127

    exponent_bits = ''
    for i in range(8):
        if exponent >= 2**(7-i):
            exponent_bits += '1'
            exponent -= 2**(7-i)
        else:
            exponent_bits += '0'

    return exponent_bits


def get_mantissa_bits(binary):
    if '.' in binary:
        integer_bits, fractional_bits = binary.split('.')
        binary = integer_bits + fractional_bits
    else:
        binary = binary.rstrip('0')

    mantissa_bits = binary[1:24]

    if len(mantissa_bits) == 23:
        last_bit = int(mantissa_bits[-1])
        second_last_bit = int(mantissa_bits[-2])
        if last_bit == 1 and second_last_bit == 1:
            mantissa_bits = mantissa_bits[:-1] + '0'
        elif last_bit == 1 or second_last_bit == 1:
            mantissa_bits = mantissa_bits[:-1] + '1'

    return mantissa_bits

def decimal_to_binary(decimal):
    if isinstance(decimal, int):
        decimal = float(decimal)
    sign_bit = get_sign_bit(decimal)

    integer_part = int(abs(decimal))
    fractional_part = float('0.' + str(abs(decimal)).split('.')[1])

    binary = ''
    if integer_part > 0:
        while integer_part > 0:
            binary = str(integer_part % 2) + binary
            integer_part //= 2
    else:
        binary = '0'

    binary += '.'
    while fractional_part > 0 and len(binary) < 25:
        fractional_part *= 2
        if fractional_part >= 1:
            binary += '1'
            fractional_part -= 1
        else:
            binary += '0'

    exponent_bits = get_exponent_bits(binary)
    mantissa_bits = get_mantissa_bits(binary)

    mantissa_bits = mantissa_bits.ljust(23, '0')

    return sign_bit + exponent_bits + mantissa_bits

def binary_ieee_to_decimal(binary):
    sign = -1 if binary[0] == "1" else 1
    exponent = int(binary[1:9], 2) - 127
    mantissa = "1" + binary[9:32]
    fraction = sum(int(mantissa[i]) * 2 ** (-i) for i in range(len(mantissa)))
    return sign * fraction * 2 ** exponent



import tkinter as tk
from PIL import Image, ImageTk

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = float(width) / float(height)

    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)

    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)

    return image.resize((width, height), resample=Image.LANCZOS)

class App:
    def __init__(self, master):
        self.master = master
        master.title("IEEE-754 Floating Point | BY SH4MIA")

        
        image = Image.open("logo.png")
        max_width, max_height = 300, 300  
        image = resize_image(image, max_width, max_height)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image=photo)
        label.image = photo
        label.pack()

        
        self.decimal_entry = tk.Entry(master, font=("Helvetica", 14))
        self.decimal_entry.pack(pady=10)

        
        self.convert_button = tk.Button(master, text="Decimal to IEEE-754", command=self.convert_to_binary,
                                        font=("Helvetica", 14))
        self.convert_button.pack(pady=10)

        
        self.binary_result = tk.Text(master, height=1, width=50, font=("Helvetica", 14))
        self.binary_result.pack(pady=10)


        
        self.binary_entry = tk.Entry(master, font=("Helvetica", 14))
        self.binary_entry.pack(pady=10)

        
        self.convert_button = tk.Button(master, text="IEEE-754 to Decimal ", command=self.convert_to_decimal,
                                        font=("Helvetica", 14))
        self.convert_button.pack(pady=10)

        
        self.decimal_result = tk.Text(master, height=1, width=50, font=("Helvetica", 14))
        self.decimal_result.pack(pady=10)

        
        self.history_label = tk.Label(master, text="Latest operations:", font=("Helvetica", 14))
        self.history_label.pack(pady=10)
        self.history = tk.Text(master, height=5, width=50, font=("Helvetica", 14))
        self.history.pack(pady=10)

        self.results_history = []


    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    def convert_to_binary(self):
        decimal_value = self.decimal_entry.get()
        if self.is_number(decimal_value) and len(decimal_value)<=10:
            decimal = float(decimal_value)
            binary = decimal_to_binary(decimal)
            self.binary_result.delete("1.0", tk.END)
            self.binary_result.insert(tk.END, binary)

            
            self.results_history.append(f"{decimal} -> {binary}")
            self.update_history()
        else:
            self.binary_result.delete("1.0", tk.END)
            self.binary_result.insert(tk.END, "Wprowadzono zły format!")

    def convert_to_decimal(self):
        binary_value = self.binary_entry.get()
        if len(binary_value) == 32 and all(bit in "01" for bit in binary_value):
            decimal = binary_ieee_to_decimal(binary_value)
            self.decimal_result.delete("1.0", tk.END)
            self.decimal_result.insert(tk.END, str(decimal))

            
            self.results_history.append(f"{binary_value} -> {decimal}")
            self.update_history()
        else:
            self.decimal_result.delete("1.0", tk.END)
            self.decimal_result.insert(tk.END, "Wprowadzono zły format!")

    def clear(self):
        self.binary_result.delete("1.0", tk.END)
        self.decimal_entry.delete(0, tk.END)
        self.binary_entry.delete(0, tk.END)
        self.decimal_result.delete("1.0", tk.END)

    def update_history(self):
        self.history.delete("1.0", tk.END)
        for result in self.results_history[-5:]:
            self.history.insert(tk.END, result + "\n")

root = tk.Tk()
app = App(root)
root.mainloop()
