import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os
import time

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("800x600")
        
        # Theme colors
        self.themes = {
            "cyber": {
                "bg": "#1a1a1a",
                "fg": "#00ffff",
                "accent": "#0066ff",
                "text": "#ffffff"
            },
            "minimal": {
                "bg": "#ffffff",
                "fg": "#ff9999",
                "accent": "#ff6666",
                "text": "#333333"
            }
        }
        self.current_theme = "cyber"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Theme switcher
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_frame = ttk.Frame(self.main_frame)
        theme_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        theme_cyber = ttk.Radiobutton(theme_frame, text="Cyber", value="cyber", 
                                    variable=self.theme_var, command=self.change_theme)
        theme_cyber.pack(side=tk.LEFT, padx=10)
        
        theme_minimal = ttk.Radiobutton(theme_frame, text="Minimal White", value="minimal", 
                                      variable=self.theme_var, command=self.change_theme)
        theme_minimal.pack(side=tk.LEFT)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.text_input = tk.Text(input_frame, height=3, width=50)
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.bind('<KeyRelease>', lambda e: self.generate_qr())
        
        # Add paste binding
        self.text_input.bind('<Control-v>', self.handle_paste)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(buttons_frame, text="Generate QR", command=self.generate_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save QR", command=self.save_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Scan Preview", command=self.show_preview).pack(side=tk.LEFT, padx=5)
        
        # QR display frame
        self.display_frame = ttk.LabelFrame(self.main_frame, text="QR Code", padding=10)
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.qr_label = ttk.Label(self.display_frame)
        self.qr_label.pack(expand=True)
        
        self.qr_image = None
        self.change_theme()
        
    def handle_paste(self, event):
        try:
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.root.clipboard_get())
            self.generate_qr()
        except:
            pass
        return "break"
        
    def generate_qr(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            return
            
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        # Apply theme colors
        fill_color = self.themes[self.current_theme]["fg"]
        back_color = self.themes[self.current_theme]["bg"]
        
        qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(qr_image)
        self.qr_label.configure(image=photo)
        self.qr_label.image = photo
        self.qr_image = qr_image
        
        # Animate fade-in
        self.animate_fade_in()
        
    def animate_fade_in(self):
        self.qr_label.place_forget()
        for i in range(0, 101, 5):
            self.qr_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.qr_label.update()
            time.sleep(0.01)
            
    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            self.qr_image.save(file_path)
            messagebox.showinfo("Success", "QR code saved successfully!")
            
    def show_preview(self):
        if not self.qr_image:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return
            
        preview = tk.Toplevel(self.root)
        preview.title("Scan Preview")
        preview.geometry("400x400")
        
        # Display QR code in actual size
        photo = ImageTk.PhotoImage(self.qr_image)
        label = ttk.Label(preview, image=photo)
        label.image = photo
        label.pack(expand=True)
        
    def change_theme(self):
        theme = self.theme_var.get()
        self.current_theme = theme
        
        # Update colors
        self.root.configure(bg=self.themes[theme]["bg"])
        self.main_frame.configure(style=f"{theme}.TFrame")
        
        # Regenerate QR code with new colors
        if self.text_input.get("1.0", tk.END).strip():
            self.generate_qr()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
