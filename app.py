import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from ui.styles import setup_styles
from ui.handlers import (
    create_save_ui, create_grayscale_ui, create_binary_ui,
    create_red_channel_ui, create_alpha_ui, create_metrics_ui,
    create_transform_ui, create_contrast_stretch_ui,
    create_histogram_equalization_ui, create_histogram_matching_ui,
    create_adaptive_histogram_ui
)
from utils.image_utils import resize_for_display, check_alpha_channel


class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Photoshop Mini")
        self.geometry("1200x700")
        self.configure(bg='#f0f0f0')

        self.original_image = None
        self.display_image = None
        self.photo_image = None
        self.current_filename = None
        self.processed_image = None
        self.original_mode = None
        self.has_alpha = False

        setup_styles()
        self._create_widgets()

    def _create_widgets(self):
        # Main container
        main_container = tk.Frame(self, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left sidebar
        left_frame = tk.Frame(main_container, bg='#34495e', width=280)
        left_frame.pack(side='left', fill='y', padx=0, pady=0)
        left_frame.pack_propagate(False)

        # Header trong sidebar
        header_frame = tk.Frame(left_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Photoshop Mini", 
                              font=('Segoe UI', 16, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=20)

        # Upload section
        upload_card = tk.Frame(left_frame, bg='#2c3e50')
        upload_card.pack(fill='x', padx=15, pady=(0, 15))

        upload_btn = tk.Button(upload_card, text="Tải ảnh lên", 
                              command=self.load_image,
                              font=('Segoe UI', 10, 'bold'),
                              bg='#3498db', fg='white',
                              relief='flat', cursor='hand2',
                              padx=20, pady=12)
        upload_btn.pack(fill='x')
        
        # Hover effect
        upload_btn.bind('<Enter>', lambda e: upload_btn.config(bg='#2980b9'))
        upload_btn.bind('<Leave>', lambda e: upload_btn.config(bg='#3498db'))

        self.filename_label = tk.Label(upload_card, 
                                      text="Chưa có tệp nào được chọn",
                                      font=('Segoe UI', 9),
                                      bg='#2c3e50', fg='#bdc3c7',
                                      wraplength=250, justify='left')
        self.filename_label.pack(fill='x', pady=(10, 0))

        # Functions list
        functions_frame = tk.Frame(left_frame, bg='#34495e')
        functions_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        func_title = tk.Label(functions_frame, text="Danh sách chức năng",
                             font=('Segoe UI', 11, 'bold'),
                             bg='#34495e', fg='white')
        func_title.pack(anchor='w', pady=(0, 10))

        # Custom listbox style
        listbox_frame = tk.Frame(functions_frame, bg='#2c3e50', relief='flat')
        listbox_frame.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')

        self.func_listbox = tk.Listbox(listbox_frame, 
                                      font=('Segoe UI', 9),
                                      bg='#2c3e50', fg='white',
                                      selectbackground='#3498db',
                                      selectforeground='white',
                                      relief='flat',
                                      highlightthickness=0,
                                      activestyle='none',
                                      yscrollcommand=scrollbar.set)
        
        funcs = [
            "Lưu ảnh sang định dạng khác",
            "Chuyển sang ảnh xám",
            "Làm ảnh nhị phân (đen trắng)",
            "Tách kênh màu Đỏ",
            "Kiểm tra kênh Alpha (RGBA)",
            "Tính 4 chỉ số (ma trận/ảnh)",
            "Biến đổi ảnh",
            "Kéo dãn độ tương phản",
            "Cân bằng histogram tiêu chuẩn",
            "Histogram Matching",
            "Cân bằng Histogram cục bộ",

        ]
        for f in funcs:
            self.func_listbox.insert(tk.END, f)
        
        self.func_listbox.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        scrollbar.config(command=self.func_listbox.yview)
        self.func_listbox.bind("<<ListboxSelect>>", self.on_function_select)

        # Right panel
        right_frame = tk.Frame(main_container, bg='#ecf0f1')
        right_frame.pack(side='left', fill='both', expand=True, padx=15, pady=15)

        # Info/Control area
        self.info_frame = tk.Frame(right_frame, bg='white', relief='flat')
        self.info_frame.pack(fill='x', pady=(0, 15))

        # Display area
        display_container = tk.Frame(right_frame, bg='white', relief='flat')
        display_container.pack(fill='both', expand=True)

        # Canvas với border đẹp
        canvas_frame = tk.Frame(display_container, bg='#bdc3c7', padx=2, pady=2)
        canvas_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='#ecf0f1', 
                               highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Text widget với style
        text_frame = tk.Frame(display_container, bg='#bdc3c7', padx=2, pady=2)
        
        self.text_widget = tk.Text(text_frame, font=('Consolas', 9),
                                  bg='#2c3e50', fg='#ecf0f1',
                                  relief='flat', padx=10, pady=10)
        text_scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=text_scrollbar.set)
        
        self.text_widget.pack(side='left', fill='both', expand=True)
        text_scrollbar.pack(side='right', fill='y')
        
        # Hide text widget initially
        text_frame.pack_forget()
        self.text_frame = text_frame

    def load_image(self):
        """Tải ảnh từ file"""
        filetypes = [
            ("Các tệp ảnh", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("Tất cả tệp", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=filetypes)
        if not path:
            return
        try:
            img = Image.open(path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở ảnh:\n{e}")
            return

        self.original_mode = img.mode
        self.has_alpha = check_alpha_channel(img)

        self.original_image = img.convert("RGBA")
        self.current_filename = os.path.basename(path)
        self.filename_label.config(text=f"📄 {self.current_filename}", fg='#2ecc71')
        self.func_listbox.selection_clear(0, tk.END)
        self.show_image(self.original_image)

    def show_image(self, pil_image):
        """Hiển thị ảnh trên canvas"""
        # Hide text widget, show canvas
        try:
            self.text_frame.pack_forget()
        except:
            pass
        self.canvas.master.pack(fill='both', expand=True)
        
        self.canvas.delete("all")
        resized = resize_for_display(self.canvas, pil_image)
        self.display_image = resized

        self.photo_image = ImageTk.PhotoImage(self.display_image)
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        self.canvas.create_image(w // 2, h // 2, image=self.photo_image, anchor="center")

    def show_text(self, content: str):
        """Hiển thị text trên text widget"""
        # Ẩn canvas, hiện text widget đẹp
        try:
            self.canvas.master.pack_forget()
        except:
            pass
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, content)
        self.text_frame.pack(fill="both", expand=True)
        self.text_widget.see("1.0")

    def on_function_select(self, event):
        """Xử lý khi chọn chức năng từ listbox"""
        sel = self.func_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        
        for child in self.info_frame.winfo_children():
            child.destroy()

        self.processed_image = None

        # Style cho info frame
        self.info_frame.config(bg='white', padx=20, pady=15)

        # Gọi UI handler tương ứng
        handlers = [
            create_save_ui,
            create_grayscale_ui,
            create_binary_ui,
            create_red_channel_ui,
            create_alpha_ui,
            create_metrics_ui,
            create_transform_ui,
            create_contrast_stretch_ui,
            create_histogram_equalization_ui,
            create_histogram_matching_ui,
            create_adaptive_histogram_ui
        ]
        
        if 0 <= idx < len(handlers):
            handlers[idx](self, self.info_frame)

    def save_as(self):
        """Lưu ảnh gốc sang định dạng khác"""
        if self.original_image is None:
            messagebox.showwarning("Lỗi", "Chưa có ảnh để lưu")
            return
        
        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        path = filedialog.asksaveasfilename(
            title="Lưu ảnh",
            defaultextension=".png",
            filetypes=filetypes
        )
        if path:
            try:
                self.original_image.save(path)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh vào:\n{path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh:\n{e}")

    def save_processed(self):
        """Lưu ảnh đã xử lý"""
        if self.processed_image is None:
            messagebox.showwarning("Lỗi", "Chưa có ảnh đã xử lý để lưu")
            return
        
        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        path = filedialog.asksaveasfilename(
            title="Lưu ảnh đã xử lý",
            defaultextension=".png",
            filetypes=filetypes
        )
        if path:
            try:
                self.processed_image.save(path)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh vào:\n{path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh:\n{e}")


def main():
    app = ImageApp()
    app.mainloop()


if __name__ == "__main__":
    main()
