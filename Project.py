import cv2
import numpy as np
import os
from tkinter import Tk, filedialog, Label, Entry, Button, messagebox, Toplevel

def encode_message(image_path, message, password):
    img = cv2.imread(image_path)

    height, width, _ = img.shape
    max_len = height * width * 3

    if len(message) > max_len:
        messagebox.showerror("Error", "Message is too long for the image.")
        return

    message += f"::{password}"  # Delimiter and password for validation

    d = {chr(i): i for i in range(256)}

    n, m, z = 0, 0, 0
    for char in message:
        img[n, m, z] = d[char]
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == width:
                m = 0
                n += 1

    encoded_path = "encoded_image.png"
    cv2.imwrite(encoded_path, img)
    messagebox.showinfo("Success", f"Message encoded! Saved as {encoded_path}")
    os.system(f"start {encoded_path}")

def decode_message(image_path, password):
    img = cv2.imread(image_path)

    height, width, _ = img.shape

    c = {i: chr(i) for i in range(256)}

    n, m, z = 0, 0, 0
    message = ""

    while True:
        message += c[img[n, m, z]]
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == width:
                m = 0
                n += 1

        if message.endswith("::" + password):
            break

    if message.endswith("::" + password):
        message = message[:-(len(password) + 2)]
        messagebox.showinfo("Decoded Message", f"Message: {message}")
    else:
        messagebox.showerror("Error", "Incorrect password!")

def open_decode_window():
    decode_window = Toplevel(app)
    decode_window.title("Decode Message")
    decode_window.geometry("400x200")

    Label(decode_window, text="Password:").pack(pady=5)
    decode_pass_entry = Entry(decode_window, width=50, show="*")
    decode_pass_entry.pack(pady=5)

    def select_image_for_decode():
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not filepath:
            return
        password = decode_pass_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter password for decryption.")
            return

        decode_message(filepath, password)

    Button(decode_window, text="Select Image to Decode", command=select_image_for_decode).pack(pady=10)

def select_image(action):
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        return

    if action == "encode":
        message = msg_entry.get()
        password = pass_entry.get()

        if not message or not password:
            messagebox.showerror("Error", "Enter both message and password.")
            return

        encode_message(filepath, message, password)

app = Tk()
app.title("Image Steganography")
app.geometry("400x300")

Label(app, text="Secret Message:").pack(pady=5)
msg_entry = Entry(app, width=50)
msg_entry.pack(pady=5)

Label(app, text="Password:").pack(pady=5)
pass_entry = Entry(app, width=50, show="*")
pass_entry.pack(pady=5)

Button(app, text="Select Image to Encode", command=lambda: select_image("encode")).pack(pady=10)
Button(app, text="Open Decode Window", command=open_decode_window).pack(pady=10)

app.mainloop()
