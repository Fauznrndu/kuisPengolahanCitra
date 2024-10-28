import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Inisialisasi aplikasi utama
root = tk.Tk()
root.title("Aplikasi Operasi Geometri")
root.geometry("800x600")

# Variabel global untuk menyimpan gambar asli dan gambar hasil
original_image = None
processed_image = None
display_original = None
display_processed = None

# Ukuran maksimal tampilan gambar
MAX_DISPLAY_SIZE = (250, 250)

# Fungsi untuk memuat gambar
def load_image():
    global original_image, display_original, processed_image
    
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        
        # Mengubah ukuran gambar jika melebihi MAX_DISPLAY_SIZE
        if original_image.width > MAX_DISPLAY_SIZE[0] or original_image.height > MAX_DISPLAY_SIZE[1]:
            original_image.thumbnail(MAX_DISPLAY_SIZE, Image.LANCZOS)
        
        display_original = ImageTk.PhotoImage(original_image)
        original_image_canvas.create_image(0, 0, anchor="nw", image=display_original)
        original_image_canvas.config(scrollregion=original_image_canvas.bbox("all"))

        processed_image = original_image.copy()
        display_processed = ImageTk.PhotoImage(processed_image)
        processed_image_canvas.create_image(0, 0, anchor="nw", image=display_processed)
        processed_image_canvas.config(scrollregion=processed_image_canvas.bbox("all"))
        
        rotate_button.config(state="normal")
        resize_button.config(state="normal")
        save_button.config(state="normal")
        reset_button.config(state="normal")

# Fungsi untuk rotasi gambar
def rotate_image():
    global processed_image, display_processed

    if original_image:
        try:
            angle = int(rotation_entry.get())
            # Reset ke gambar asli setiap kali melakukan rotasi
            processed_image = original_image.copy()
            
            # Putar gambar dengan sudut yang dimasukkan
            rotated_image = processed_image.rotate(angle)
            
            # Mengubah ukuran gambar yang dirotasi sesuai MAX_DISPLAY_SIZE
            if rotated_image.width > MAX_DISPLAY_SIZE[0] or rotated_image.height > MAX_DISPLAY_SIZE[1]:
                rotated_image.thumbnail(MAX_DISPLAY_SIZE, Image.LANCZOS)

            display_processed = ImageTk.PhotoImage(rotated_image)
            processed_image_canvas.create_image(0, 0, anchor="nw", image=display_processed)
            processed_image_canvas.config(scrollregion=processed_image_canvas.bbox("all"))
            processed_image = rotated_image

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka valid untuk sudut rotasi.")

# Fungsi untuk mengubah ukuran gambar
def resize_image():
    global processed_image, display_processed
    
    if processed_image:
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            resized_image = processed_image.resize((width, height), Image.LANCZOS)
            
            display_processed = ImageTk.PhotoImage(resized_image)
            processed_image_canvas.create_image(0, 0, anchor="nw", image=display_processed)
            processed_image_canvas.config(scrollregion=processed_image_canvas.bbox("all"))
            processed_image = resized_image

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka valid untuk ukuran gambar.")

# Fungsi untuk menyimpan gambar hasil
def save_image():
    if processed_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", ".")])
        if file_path:
            processed_image.save(file_path)
            messagebox.showinfo("Simpan Gambar", "Gambar berhasil disimpan!")

# Fungsi untuk mereset gambar ke kondisi awal
def reset_image():
    global processed_image, display_processed
    
    if original_image:
        processed_image = original_image.copy()
        display_processed = ImageTk.PhotoImage(processed_image)
        processed_image_canvas.create_image(0, 0, anchor="nw", image=display_processed)
        processed_image_canvas.config(scrollregion=processed_image_canvas.bbox("all"))

# Frame untuk menampung gambar dan kontrol
image_frame = tk.Frame(root)
image_frame.pack()

# Canvas dan scrollbar untuk gambar asli
original_image_canvas = tk.Canvas(image_frame, width=MAX_DISPLAY_SIZE[0], height=MAX_DISPLAY_SIZE[1])
original_image_canvas.grid(row=0, column=0, padx=10, pady=10)
original_scrollbar_y = tk.Scrollbar(image_frame, orient="vertical", command=original_image_canvas.yview)
original_scrollbar_y.grid(row=0, column=1, sticky="ns")
original_image_canvas.config(yscrollcommand=original_scrollbar_y.set)

# Canvas dan scrollbar untuk gambar hasil
processed_image_canvas = tk.Canvas(image_frame, width=MAX_DISPLAY_SIZE[0], height=MAX_DISPLAY_SIZE[1])
processed_image_canvas.grid(row=0, column=2, padx=10, pady=10)
processed_scrollbar_y = tk.Scrollbar(image_frame, orient="vertical", command=processed_image_canvas.yview)
processed_scrollbar_y.grid(row=0, column=3, sticky="ns")
processed_image_canvas.config(yscrollcommand=processed_scrollbar_y.set)

# Scrollbar horizontal untuk gambar hasil
processed_scrollbar_x = tk.Scrollbar(image_frame, orient="horizontal", command=processed_image_canvas.xview)
processed_scrollbar_x.grid(row=1, column=2, sticky="ew")
processed_image_canvas.config(xscrollcommand=processed_scrollbar_x.set)

# Frame untuk kontrol rotasi dan skala
control_frame = tk.Frame(root)
control_frame.pack()

# Tombol untuk memuat gambar
load_button = tk.Button(control_frame, text="Muat Gambar", command=load_image)
load_button.grid(row=0, column=0, pady=5)

# Input dan tombol untuk rotasi
rotation_label = tk.Label(control_frame, text="Sudut Rotasi (derajat):")
rotation_label.grid(row=1, column=0, pady=5)
rotation_entry = tk.Entry(control_frame)
rotation_entry.grid(row=1, column=1, pady=5)

rotate_button = tk.Button(control_frame, text="Rotasi Gambar", command=rotate_image, state="disabled")
rotate_button.grid(row=1, column=2, pady=5)

# Input untuk ukuran baru gambar (lebar dan tinggi)
width_label = tk.Label(control_frame, text="Lebar Baru:")
width_label.grid(row=2, column=0, pady=5)
width_entry = tk.Entry(control_frame)
width_entry.grid(row=2, column=1, pady=5)

height_label = tk.Label(control_frame, text="Tinggi Baru:")
height_label.grid(row=3, column=0, pady=5)
height_entry = tk.Entry(control_frame)
height_entry.grid(row=3, column=1, pady=5)

resize_button = tk.Button(control_frame, text="Ubah Ukuran", command=resize_image, state="disabled")
resize_button.grid(row=3, column=2, pady=5)

# Tombol untuk menyimpan gambar hasil
save_button = tk.Button(control_frame, text="Simpan Gambar", command=save_image, state="disabled")
save_button.grid(row=4, column=1, pady=5)

# Tombol untuk mereset gambar
reset_button = tk.Button(control_frame, text="Reset Gambar", command=reset_image, state="disabled")
reset_button.grid(row=4, column=0, pady=5)

# Jalankan aplikasi
root.mainloop()