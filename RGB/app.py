import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


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

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """Thiết lập style đẹp cho các widget"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style cho Frame
        style.configure('Card.TFrame', background='white', relief='flat')
        style.configure('Sidebar.TFrame', background='#2c3e50')
        
        # Style cho Label
        style.configure('Title.TLabel', font=('Segoe UI', 11, 'bold'), 
                       background='white', foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 9), 
                       background='white', foreground='#7f8c8d')
        style.configure('Sidebar.TLabel', font=('Segoe UI', 9), 
                       background='#2c3e50', foreground='white')
        
        # Style cho Button
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'),
                       padding=10, background='#3498db', foreground='white')
        style.configure('Secondary.TButton', font=('Segoe UI', 9),
                       padding=8, background='#95a5a6')
        style.configure('Success.TButton', font=('Segoe UI', 9),
                       padding=8, background='#27ae60', foreground='white')
        
        # Style cho LabelFrame
        style.configure('Card.TLabelframe', background='white', 
                       relief='flat', borderwidth=2)
        style.configure('Card.TLabelframe.Label', font=('Segoe UI', 10, 'bold'),
                       background='white', foreground='#2c3e50')

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
            "Kéo dãn độ tương phản"
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
        try:
            self.has_alpha = ("A" in img.getbands())
        except Exception:
            self.has_alpha = False

        self.original_image = img.convert("RGBA")
        self.current_filename = os.path.basename(path)
        self.filename_label.config(text=f"📄 {self.current_filename}", fg='#2ecc71')
        self.func_listbox.selection_clear(0, tk.END)
        self.show_image(self.original_image)

    def show_image(self, pil_image):
        # Hide text widget, show canvas
        try:
            self.text_frame.pack_forget()
        except:
            pass
        self.canvas.master.pack(fill='both', expand=True)
        
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        img_w, img_h = pil_image.size
        ratio = min(w / img_w, h / img_h, 1.0)
        new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
        self.display_image = pil_image.resize(new_size, Image.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.create_image(w // 2, h // 2, image=self.photo_image, anchor="center")

    def on_function_select(self, event):
        sel = self.func_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        
        for child in self.info_frame.winfo_children():
            child.destroy()

        self.processed_image = None

        # Style cho info frame
        self.info_frame.config(bg='white', padx=20, pady=15)

        if idx == 0:
            self._show_save_function()
        elif idx == 1:
            self._show_grayscale_function()
        elif idx == 2:
            self._show_binary_function()
        elif idx == 3:
            self._show_red_channel_function()
        elif idx == 4:
            self._show_alpha_function()
        elif idx == 5:
            self._show_metrics_function()
        elif idx == 6:
            self._show_transform_function()
        elif idx == 7:
            self._show_contrast_stretch_function()


    def _show_save_function(self):
        title = tk.Label(self.info_frame, text="Lưu ảnh sang định dạng khác",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        desc = tk.Label(self.info_frame, 
                       text="Chọn định dạng mới để lưu ảnh gốc của bạn",
                       font=('Segoe UI', 9),
                       bg='white', fg='#7f8c8d')
        desc.pack(anchor='w', pady=(0, 15))
        
        save_btn = tk.Button(self.info_frame, text="💾 Lưu ảnh...", 
                           command=self.save_as,
                           font=('Segoe UI', 10, 'bold'),
                           bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2',
                           padx=20, pady=10)
        save_btn.pack(anchor='w')

    def _show_grayscale_function(self):
        title = tk.Label(self.info_frame, text="Chuyển ảnh xám",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                    font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return
        
        gray = self.apply_grayscale()
        if gray is not None:
            self.processed_image = gray
            self.show_image(self.processed_image)
        
        btn_frame = tk.Frame(self.info_frame, bg='white')
        btn_frame.pack(anchor='w', pady=(10, 0))
        
        save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                           command=self.save_processed,
                           font=('Segoe UI', 9), bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2', padx=15, pady=8)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        revert_btn = tk.Button(btn_frame, text="Quay về ảnh gốc",
                             command=lambda: self.show_image(self.original_image),
                             font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                             relief='flat', cursor='hand2', padx=15, pady=8)
        revert_btn.grid(row=0, column=1)

    def _show_binary_function(self):
        title = tk.Label(self.info_frame, text="⬛ Làm ảnh nhị phân",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                    font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return
        
        base_gray = self.original_image.convert("L")
        
        slider_frame = tk.Frame(self.info_frame, bg='white')
        slider_frame.pack(anchor='w', fill='x', pady=(0, 10))
        
        tk.Label(slider_frame, text="Ngưỡng:", font=('Segoe UI', 9, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        slider = tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                         length=400, bg='white', highlightthickness=0,
                         troughcolor='#ecf0f1', fg='#2c3e50')
        slider.set(128)
        slider.pack(anchor='w', fill='x')

        def on_threshold(val):
            try:
                t = int(float(val))
            except Exception:
                t = 128
            bw = base_gray.point(lambda p: 255 if p >= t else 0).convert("RGBA")
            self.processed_image = bw
            self.show_image(self.processed_image)

        slider.config(command=on_threshold)
        on_threshold(slider.get())

        btn_frame = tk.Frame(self.info_frame, bg='white')
        btn_frame.pack(anchor='w')
        
        save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                           command=self.save_processed,
                           font=('Segoe UI', 9), bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2', padx=15, pady=8)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        revert_btn = tk.Button(btn_frame, text="Quay về ảnh gốc",
                             command=lambda: self.show_image(self.original_image),
                             font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                             relief='flat', cursor='hand2', padx=15, pady=8)
        revert_btn.grid(row=0, column=1)

    def _show_red_channel_function(self):
        title = tk.Label(self.info_frame, text="Tách kênh màu Đỏ",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                    font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return
        
        try:
            rgb = self.original_image.convert("RGB")
            r, g, b = rgb.split()
            zero = Image.new("L", r.size, 0)
            red_only = Image.merge("RGB", (r, zero, zero)).convert("RGBA")
            self.processed_image = red_only
            self.show_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Lỗi xử lý", f"Không thể tách kênh đỏ:\n{e}")
            return

        btn_frame = tk.Frame(self.info_frame, bg='white')
        btn_frame.pack(anchor='w', pady=(10, 0))
        
        save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                           command=self.save_processed,
                           font=('Segoe UI', 9), bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2', padx=15, pady=8)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        revert_btn = tk.Button(btn_frame, text="↩️ Quay về ảnh gốc",
                             command=lambda: self.show_image(self.original_image),
                             font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                             relief='flat', cursor='hand2', padx=15, pady=8)
        revert_btn.grid(row=0, column=1)

    def _show_alpha_function(self):
        title = tk.Label(self.info_frame, text="Kiểm tra kênh Alpha",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                    font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return

        info_lines = []
        w, h = self.original_image.size
        info_lines.append(f"Kích thước: {w} x {h}")
        info_lines.append(f"Chế độ ban đầu: {self.original_mode}")
        info_lines.append(f"Có kênh Alpha: {self.has_alpha}")

        if not self.has_alpha:
            info_lines.append("")
            info_lines.append("Ảnh không có kênh Alpha")
            self.show_text('\n'.join(info_lines))
            return

        try:
            alpha = self.original_image.split()[3]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tách kênh Alpha:\n{e}")
            return

        alpha_img_for_display = alpha.convert("L").convert("RGBA")
        self.processed_image = alpha_img_for_display
        self.show_image(self.processed_image)

        max_cells = 2000
        total = w * h
        info_lines.append("")
        if total <= max_cells:
            info_lines.append("Ma trận Alpha (0-255) theo hàng:")
            pixels = list(alpha.getdata())
            for y in range(h):
                row = pixels[y * w:(y + 1) * w]
                info_lines.append(' '.join(str(p) for p in row))
        else:
            info_lines.append("Ảnh quá lớn để hiện ma trận đầy đủ. Hiển thị mẫu 10x10:")
            sample_w = min(10, w)
            sample_h = min(10, h)
            pixels = list(alpha.getdata())
            for y in range(sample_h):
                row = pixels[y * w:y * w + sample_w]
                info_lines.append(' '.join(str(p) for p in row))

        self.show_text('\n'.join(info_lines))

    def _show_metrics_function(self):
        title = tk.Label(self.info_frame, text="Tính 4 chỉ số",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 5))
        
        desc = tk.Label(self.info_frame, 
                       text="Độ sáng, Độ tương phản, Entropy, Độ sắc nét",
                       font=('Segoe UI', 9),
                       bg='white', fg='#7f8c8d')
        desc.pack(anchor='w', pady=(0, 15))
        
        btn_frame = tk.Frame(self.info_frame, bg='white')
        btn_frame.pack(anchor='w')
        
        btns = [
            ("Ma trận M mẫu", self.run_on_test_matrix),
            ("Ma trận con A,B,C", self.run_on_submatrices),
            ("Ảnh đã tải", self.run_on_loaded_image)
        ]
        
        for i, (text, cmd) in enumerate(btns):
            btn = tk.Button(btn_frame, text=text, command=cmd,
                          font=('Segoe UI', 9), bg='#3498db', fg='white',
                          relief='flat', cursor='hand2', padx=15, pady=8)
            btn.grid(row=i, column=0, pady=5, sticky='ew')

    def _show_transform_function(self):
        title = tk.Label(self.info_frame, text="Biến đổi ảnh",
                        font=('Segoe UI', 12, 'bold'),
                        bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))
        
        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                    font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return

        ops_frame = tk.Frame(self.info_frame, bg='white')
        ops_frame.pack(anchor='w', pady=(0, 10), fill='x')

        tk.Label(ops_frame, text="Chọn phép biến đổi:",
                font=('Segoe UI', 9, 'bold'),
                bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
        
        op_var = tk.StringVar(value="Âm bản")
        op_menu = ttk.Combobox(ops_frame, textvariable=op_var,
                              values=["Âm bản", "Logarit", "Logarit ngược", "Gamma"],
                              state="readonly", width=20)
        op_menu.grid(row=0, column=1, padx=(10, 0), pady=5)

        slider_frame = tk.Frame(self.info_frame, bg='white')
        slider_frame.pack(anchor='w', fill='x', pady=(0, 10))

        c_var = tk.DoubleVar(value=1.0)
        base_var = tk.DoubleVar(value=2.718)
        gamma_var = tk.DoubleVar(value=1.0)

        def refresh_sliders(*args):
            for widget in slider_frame.winfo_children():
                widget.destroy()

            sel = op_var.get()

            if sel == "Âm bản":
                tk.Label(slider_frame, text="Âm bản không cần tham số",
                        font=('Segoe UI', 9, 'italic'),
                        bg='white', fg='#7f8c8d').pack(anchor='w')

            if sel in ["Logarit", "Logarit ngược"]:
                tk.Label(slider_frame, text="Hằng số c:",
                        font=('Segoe UI', 9, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w', pady=(5, 0))
                tk.Scale(slider_frame, variable=c_var, from_=0.1, to=5.0,
                        resolution=0.1, orient=tk.HORIZONTAL, length=300,
                        bg='white', highlightthickness=0,
                        troughcolor='#ecf0f1', fg='#2c3e50').pack(anchor='w')

                tk.Label(slider_frame, text="Cơ số log:",
                        font=('Segoe UI', 9, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w', pady=(5, 0))
                tk.Scale(slider_frame, variable=base_var, from_=1.1, to=10.0,
                        resolution=0.1, orient=tk.HORIZONTAL, length=300,
                        bg='white', highlightthickness=0,
                        troughcolor='#ecf0f1', fg='#2c3e50').pack(anchor='w')

            if sel == "Gamma":
                tk.Label(slider_frame, text="Gamma:",
                        font=('Segoe UI', 9, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w', pady=(5, 0))
                tk.Scale(slider_frame, variable=gamma_var, from_=0.1, to=5.0,
                        resolution=0.1, orient=tk.HORIZONTAL, length=300,
                        bg='white', highlightthickness=0,
                        troughcolor='#ecf0f1', fg='#2c3e50').pack(anchor='w')

        op_menu.bind("<<ComboboxSelected>>", refresh_sliders)
        refresh_sliders()

        btn_frame = tk.Frame(self.info_frame, bg='white')
        btn_frame.pack(anchor='w', pady=(10, 0))

        def _map_and_apply():
            sel = op_var.get()
            mapping = {
                'Âm bản': 'invert',
                'Logarit': 'log',
                'Logarit ngược': 'invlog',
                'Gamma': 'gamma'
            }
            op_code = mapping.get(sel, 'invert')
            self.apply_pixel_transform(op_code, c_var.get(), base_var.get(), gamma_var.get())

        apply_btn = tk.Button(btn_frame, text="Áp dụng", command=_map_and_apply,
                            font=('Segoe UI', 9, 'bold'), bg='#3498db', fg='white',
                            relief='flat', cursor='hand2', padx=15, pady=8)
        apply_btn.grid(row=0, column=0, padx=(0, 10))
        
        save_btn = tk.Button(btn_frame, text="Lưu", command=self.save_processed,
                           font=('Segoe UI', 9), bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2', padx=15, pady=8)
        save_btn.grid(row=0, column=1, padx=(0, 10))
        
        revert_btn = tk.Button(btn_frame, text="Quay về", 
                             command=lambda: self.show_image(self.original_image),
                             font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                             relief='flat', cursor='hand2', padx=15, pady=8)
        revert_btn.grid(row=0, column=2)

    def apply_grayscale(self):
        if self.original_image is None:
            return None
        gray = self.original_image.convert("L").convert("RGBA")
        return gray

    def show_text(self, content: str):
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

    def compute_metrics_from_array(self, arr: np.ndarray):
        a = np.asarray(arr, dtype=float)

        mean = float(np.mean(a))
        contrast = float(np.std(a))

        vals = a.ravel()
        if np.issubdtype(a.dtype, np.integer) or np.all(np.mod(vals, 1) == 0):
            unique, counts = np.unique(vals, return_counts=True)
            probs = counts / counts.sum()
        else:
            counts, _ = np.histogram(vals, bins=256, range=(vals.min(), vals.max()))
            probs = counts / counts.sum()
        probs = probs[probs > 0]
        entropy = float(-(probs * np.log2(probs)).sum())

        # Laplacian
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], float)
        pad = np.pad(a, pad_width=1, mode='edge')

        h, w = a.shape
        gx = np.zeros_like(a)
        gy = np.zeros_like(a)

        for y in range(h):
            for x in range(w):
                region = pad[y:y+3, x:x+3]
                gx[y, x] = np.sum(region * sobel_x)
                gy[y, x] = np.sum(region * sobel_y)

        sharpness = float(np.mean(np.sqrt(gx**2 + gy**2)))

        return {
            "mean": mean,
            "contrast": contrast,
            "entropy": entropy,
            "sharpness": sharpness
        }

    def format_metrics(self, name: str, metrics: dict):
        return (
            f"{name}:\n"
            f"  • Độ sáng trung bình: {metrics['mean']:.4f}\n"
            f"  • Độ tương phản: {metrics['contrast']:.4f}\n"
            f"  • Entropy: {metrics['entropy']:.6f}\n"
            f"  • Độ sắc nét (Laplacian): {metrics['sharpness']:.6f}\n"
        )

    def run_on_test_matrix(self):
        M = np.array([
            [1,1,1,1,1,1,1,1,1,1],
            [1,2,2,3,1,1,1,7,2,1],
            [1,2,3,2,1,1,5,3,6,1],
            [1,3,2,2,1,1,0,4,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,1,1,1,1,1],
            [1,0,7,7,1,1,1,1,1,1],
            [1,0,7,7,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
        ], dtype=float)

        m = self.compute_metrics_from_array(M)
        self.show_text(self.format_metrics("Ma trận M (10x10)", m))

    def run_on_submatrices(self):
        M = np.array([
            [1,1,1,1,1,1,1,1,1,1],
            [1,2,2,3,1,1,1,7,2,1],
            [1,2,3,2,1,1,5,3,6,1],
            [1,3,2,2,1,1,0,4,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,1,1,1,1,1],
            [1,0,7,7,1,1,1,1,1,1],
            [1,0,7,7,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
        ], dtype=float)

        A = M[1:4, 1:4]
        B = M[6:9, 1:4]
        C = M[1:4, 5:8]

        text = ""
        text += self.format_metrics("Ma trận A", self.compute_metrics_from_array(A))
        text += "\n"
        text += self.format_metrics("Ma trận B", self.compute_metrics_from_array(B))
        text += "\n"
        text += self.format_metrics("Ma trận C", self.compute_metrics_from_array(C))

        self.show_text(text)

    def run_on_loaded_image(self):
        if self.original_image is None:
            messagebox.showwarning("Chưa có ảnh", "Hãy tải ảnh lên trước.")
            return
        gray = self.original_image.convert("L")
        arr = np.array(gray, float)
        metrics = self.compute_metrics_from_array(arr)
        self.show_text(self.format_metrics(f"Ảnh: {self.current_filename}", metrics))

    def apply_pixel_transform(self, op: str, c: float, base: float, gamma: float):
        if self.original_image is None:
            messagebox.showwarning("Chưa có ảnh", "Hãy tải ảnh trước.")
            return

        img = self.original_image.convert("RGB")
        arr = np.array(img, dtype=float)
        out = np.zeros_like(arr)

        for ch in range(3):
            r = arr[:, :, ch]

            if op == "invert":
                s = 255 - r

            elif op == "log":
                x = r / 255
                if base <= 0 or base == 1:
                    messagebox.showerror("Lỗi", "Cơ số log không hợp lệ.")
                    return
                ln = np.log(1 + x)
                s = c * (ln / np.log(base))
                s = (s - s.min()) / (s.max() - s.min()) * 255

            elif op == "invlog":
                x = r / 255
                s = base ** (x / c) - 1
                s = (s - s.min()) / (s.max() - s.min()) * 255

            elif op == "gamma":
                x = r / 255
                s = (x ** gamma) * 255

            out[:, :, ch] = s

        out = np.clip(out, 0, 255).astype(np.uint8)

        if self.has_alpha:
            alpha = np.array(self.original_image.split()[3])
            result = Image.fromarray(out, "RGB").convert("RGBA")
            result.putalpha(Image.fromarray(alpha))
        else:
            result = Image.fromarray(out, "RGB").convert("RGBA")

        self.processed_image = result
        self.show_image(result)
    def _show_contrast_stretch_function(self):
        title = tk.Label(self.info_frame, text="Kéo dãn độ tương phản",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
        title.pack(anchor='w', pady=(0, 10))

        if self.original_image is None:
            tk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
            return

        # Frame chọn loại
        mode_var = tk.StringVar(value="linear")
        mode_frame = tk.Frame(self.info_frame, bg='white')
        mode_frame.pack(anchor='w')

        tk.Radiobutton(mode_frame, text="Loại 1 (Tuyến tính)", variable=mode_var,
                    value="linear", bg='white',
                    command=lambda: refresh_sliders()).pack(anchor='w')

        tk.Radiobutton(mode_frame, text="Loại 2 (Từng phần)", variable=mode_var,
                    value="piecewise", bg='white',
                    command=lambda: refresh_sliders()).pack(anchor='w')

        # Frame chứa sliders
        slider_frame = tk.Frame(self.info_frame, bg='white')
        slider_frame.pack(anchor='w', pady=10)

        # Các biến
        r_min_var = tk.IntVar(value=50)
        r_max_var = tk.IntVar(value=200)
        l0_var = tk.IntVar(value=50)
        l1_var = tk.IntVar(value=200)

        def apply_now(*args):
            self.apply_contrast_stretch(
                mode_var.get(),
                r_min_var.get(),
                r_max_var.get(),
                l0_var.get(),
                l1_var.get()
            )

        def add_slider(parent, text, var, frm=0, to=255):
            tk.Label(parent, text=text, bg='white',
                    font=('Segoe UI', 9, 'bold')).pack(anchor='w')
            scale = tk.Scale(parent, variable=var, from_=frm, to=to,
                            orient=tk.HORIZONTAL, length=300,
                            bg='white', highlightthickness=0,
                            troughcolor='#ecf0f1',
                            command=apply_now)
            scale.pack(anchor='w', pady=2)
            return scale

        def refresh_sliders():
            for widget in slider_frame.winfo_children():
                widget.destroy()

            # Slider chung cho cả hai loại
            add_slider(slider_frame, "r_min", r_min_var, 0, 255)
            add_slider(slider_frame, "r_max", r_max_var, 0, 255)

            if mode_var.get() == "piecewise":
                add_slider(slider_frame, "l0 (vùng tối)", l0_var, 0, 255)
                add_slider(slider_frame, "l1 (vùng sáng)", l1_var, 0, 255)

            apply_now()

        refresh_sliders()


    def contrast_stretch_piecewise(self, arr, r_min, r_max, l0=50, l1=200):
        arr = arr.astype(float)
        out = np.zeros_like(arr)

        # tối
        mask1 = arr <= r_min
        out[mask1] = (arr[mask1] / r_min) * l0

        # giữa
        mask2 = (arr > r_min) & (arr <= r_max)
        out[mask2] = ((arr[mask2] - r_min) / (r_max - r_min)) * (l1 - l0) + l0

        # sáng
        mask3 = arr > r_max
        out[mask3] = ((arr[mask3] - r_max) / (255 - r_max)) * (255 - l1) + l1

        return np.clip(out, 0, 255)

    def apply_contrast_stretch(self, mode, r_min, r_max, l0, l1):
        if self.original_image is None:
            messagebox.showwarning("Lỗi", "Chưa có ảnh!")
            return

        img = self.original_image.convert("RGB")
        arr = np.array(img, float)
        out = np.zeros_like(arr)

        for ch in range(3):
            channel = arr[:, :, ch]
            if mode == "linear":
                out[:, :, ch] = self.contrast_stretch_linear(channel, r_min, r_max)
            else:
                out[:, :, ch] = self.contrast_stretch_piecewise(channel, r_min, r_max, l0, l1)

        out = np.clip(out, 0, 255).astype(np.uint8)
        result = Image.fromarray(out, "RGB").convert("RGBA")

        self.processed_image = result
        self.show_image(result)
    def contrast_stretch_linear(self, arr, r_min, r_max):
        arr = arr.astype(float)

        # tránh chia cho 0
        if r_max <= r_min:
            return arr

        out = (arr - r_min) * (255.0 / (r_max - r_min))

        # pixel < r_min → 0
        out[arr < r_min] = 0

        # pixel > r_max → 255
        out[arr > r_max] = 255

        return np.clip(out, 0, 255)


def main():
    app = ImageApp()
    app.mainloop()


if __name__ == "__main__":
    main()