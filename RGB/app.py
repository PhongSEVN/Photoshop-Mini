import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Photoshop - Mini App")
        self.geometry("1000x650")

        self.original_image = None
        self.display_image = None
        self.photo_image = None
        self.current_filename = None
        self.processed_image = None
        self.original_mode = None
        self.has_alpha = False

        self._create_widgets()

    def _create_widgets(self):
        # Left column (controls)
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

        # Top-left: Upload
        upload_frame = ttk.Frame(left_frame)
        upload_frame.grid(row=0, column=0, sticky="ew", pady=(0,12))

        upload_btn = ttk.Button(upload_frame, text="Tải ảnh lên...", command=self.load_image)
        upload_btn.pack(fill="x")

        self.filename_label = ttk.Label(upload_frame, text="Chưa có tệp nào được chọn", wraplength=220)
        self.filename_label.pack(fill="x", pady=(6,0))

        # Bottom-left: Function list
        functions_frame = ttk.Labelframe(left_frame, text="Danh sách chức năng")
        functions_frame.grid(row=1, column=0, sticky="nsew")
        functions_frame.config(width=240, height=400)

        self.func_listbox = tk.Listbox(functions_frame, height=10, exportselection=False)
        funcs = [
            "Lưu ảnh sang định dạng khác",
            "Chuyển sang ảnh xám",
            "Làm ảnh nhị phân (đen trắng)",
            "Tách kênh màu Đỏ",
            "Kiểm tra kênh Alpha (RGBA)",
            "Tính 4 chỉ số (ma trận/ảnh)",
            "Biến đổi ảnh",
        ]
        for f in funcs:
            self.func_listbox.insert(tk.END, f)
        self.func_listbox.pack(fill="both", expand=True, padx=6, pady=6)
        self.func_listbox.bind("<<ListboxSelect>>", self.on_function_select)

        # Right: Display area. Layout: top = info_frame, bottom = display_frame (canvas/text)
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Info label / dynamic controls (top of right frame)
        self.info_frame = ttk.Frame(right_frame)
        self.info_frame.grid(row=0, column=0, sticky="ew")

        # Display frame (holds canvas and text widget) below info_frame
        display_frame = ttk.Frame(right_frame)
        display_frame.grid(row=1, column=0, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Canvas for image (inside display_frame)
        self.canvas = tk.Canvas(display_frame, bg="#ddd")
        self.canvas.pack(fill="both", expand=True)

        # Text widget for showing matrix/info (hidden by default)
        self.text_widget = tk.Text(display_frame)
        self.text_widget.pack_forget()

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

        # Lưu thông tin ban đầu để biết có kênh Alpha hay không
        self.original_mode = img.mode
        try:
            self.has_alpha = ("A" in img.getbands())
        except Exception:
            self.has_alpha = False

        # Chuẩn hoá ảnh nội bộ sang RGBA để xử lý/hiển thị dễ dàng
        self.original_image = img.convert("RGBA")
        self.current_filename = os.path.basename(path)
        self.filename_label.config(text=self.current_filename)
        self.func_listbox.selection_clear(0, tk.END)
        self.show_image(self.original_image)

    def show_image(self, pil_image):
        # Resize to fit canvas while keeping aspect ratio
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
        # Clear info controls
        for child in self.info_frame.winfo_children():
            child.destroy()

        # Clear processed image by default (will be set when processing)
        self.processed_image = None

        if idx == 0:
            # show save button
            ttk.Label(self.info_frame, text="Lưu ảnh sang định dạng khác").pack(anchor="w")
            save_btn = ttk.Button(self.info_frame, text="Lưu ảnh...", command=self.save_as)
            save_btn.pack(anchor="w", pady=(6,0))
            ttk.Label(self.info_frame, text="(Chức năng này sẽ lưu ảnh gốc sang định dạng khác)").pack(anchor="w", pady=(6,0))
        elif idx == 1:
            # Chuyển ảnh xám
            ttk.Label(self.info_frame, text="Chuyển ảnh xám").pack(anchor="w")
            if self.original_image is None:
                ttk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.").pack(anchor="w", pady=(6,0))
                return
            # apply grayscale and show
            gray = self.apply_grayscale()
            if gray is not None:
                self.processed_image = gray
                self.show_image(self.processed_image)
            # controls: save processed and revert
            save_btn = ttk.Button(self.info_frame, text="Lưu kết quả...", command=self.save_processed)
            save_btn.pack(anchor="w", pady=(6,4))
            revert_btn = ttk.Button(self.info_frame, text="Quay về ảnh gốc", command=lambda: self.show_image(self.original_image))
            revert_btn.pack(anchor="w")
            ttk.Label(self.info_frame, text="Ảnh được chuyển sang thang xám và hiển thị ở bên phải.").pack(anchor="w", pady=(6,0))
        elif idx == 2:
            ttk.Label(self.info_frame, text="Làm ảnh nhị phân (đen trắng)").pack(anchor="w")
            if self.original_image is None:
                ttk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.").pack(anchor="w", pady=(6,0))
                return
            base_gray = self.original_image.convert("L")
            # Slider
            slider = tk.Scale(self.info_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Ngưỡng", length=200)
            slider.set(128)
            slider.pack(anchor="w", pady=(6,4))

            def on_threshold(val):
                try:
                    t = int(float(val))
                except Exception:
                    t = 128
                bw = base_gray.point(lambda p: 255 if p >= t else 0).convert("RGBA")
                self.processed_image = bw
                self.show_image(self.processed_image)

            slider.config(command=on_threshold)
            # initial apply
            on_threshold(slider.get())

            save_btn = ttk.Button(self.info_frame, text="Lưu kết quả...", command=self.save_processed)
            save_btn.pack(anchor="w", pady=(6,4))
            revert_btn = ttk.Button(self.info_frame, text="Quay về ảnh gốc", command=lambda: self.show_image(self.original_image))
            revert_btn.pack(anchor="w")
        elif idx == 3:
            # Tách kênh màu Đỏ (Red channel)
            ttk.Label(self.info_frame, text="Tách kênh màu Đỏ (Red channel)").pack(anchor="w")
            if self.original_image is None:
                ttk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.").pack(anchor="w", pady=(6,0))
                return
            # Tách kênh đỏ: giữ ma trận kênh R, đặt G và B về 0
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

            save_btn = ttk.Button(self.info_frame, text="Lưu kết quả...", command=self.save_processed)
            save_btn.pack(anchor="w", pady=(6,4))
            revert_btn = ttk.Button(self.info_frame, text="Quay về ảnh gốc", command=lambda: self.show_image(self.original_image))
            revert_btn.pack(anchor="w")
            ttk.Label(self.info_frame, text="Ảnh hiển thị chỉ giữ kênh đỏ (G,B = 0)").pack(anchor="w", pady=(6,0))
        elif idx == 4:
            # Kiểm tra kênh Alpha (32-bit) và tách ma trận Alpha
            ttk.Label(self.info_frame, text="Kiểm tra kênh Alpha (32-bit)").pack(anchor="w")
            if self.original_image is None:
                ttk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.").pack(anchor="w", pady=(6,0))
                return

            info_lines = []
            w, h = self.original_image.size
            info_lines.append(f"Kích thước: {w} x {h}")
            info_lines.append(f"Chế độ ban đầu: {self.original_mode}")
            info_lines.append(f"Có kênh Alpha: {self.has_alpha}")

            if not self.has_alpha:
                info_lines.append("")
                info_lines.append("Ảnh không có kênh Alpha")
                # Show message text
                self.show_text('\n'.join(info_lines))
                return

            try:
                alpha = self.original_image.split()[3]  # L image
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tách kênh Alpha:\n{e}")
                return

            alpha_img_for_display = alpha.convert("L").convert("RGBA")
            self.processed_image = alpha_img_for_display
            self.show_image(self.processed_image)

            # Prepare textual matrix if small
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
                info_lines.append("Ảnh quá lớn để hiện ma trận đầy đủ. Hiển thị mẫu 10x10 góc trên trái:")
                sample_w = min(10, w)
                sample_h = min(10, h)
                pixels = list(alpha.getdata())
                for y in range(sample_h):
                    row = pixels[y * w:y * w + sample_w]
                    info_lines.append(' '.join(str(p) for p in row))

            # Hiện phần thông tin bên trong text widget (dưới ảnh)
            self.show_text('\n'.join(info_lines))
        elif idx == 5:
            # Tính 4 chỉ số (Độ sáng trung bình, Độ tương phản, Entropy, Độ sắc nét)
            ttk.Label(self.info_frame, text="Tính 4 chỉ số: Độ sáng, Độ tương phản, Entropy, Độ sắc nét").pack(anchor="w")
            # Buttons: chạy trên ma trận mẫu M, chạy trên ma trận con, chạy trên ảnh đã load
            run_btn = ttk.Button(self.info_frame, text="Chạy trên ma trận M mẫu", command=self.run_on_test_matrix)
            run_btn.pack(anchor="w", pady=(6,4))

            run_sub_btn = ttk.Button(self.info_frame, text="Chạy trên ma trận con A,B,C", command=self.run_on_submatrices)
            run_sub_btn.pack(anchor="w", pady=(0,4))

            run_img_btn = ttk.Button(self.info_frame, text="Chạy trên ảnh (convert -> grayscale)", command=self.run_on_loaded_image)
            run_img_btn.pack(anchor="w", pady=(0,4))

            ttk.Label(self.info_frame, text="Kết quả sẽ hiển thị ở khu vực bên phải (dạng văn bản).").pack(anchor="w", pady=(6,0))
        elif idx == 6:
            ttk.Label(self.info_frame, text="Biến đổi ảnh").pack(anchor="w")
            if self.original_image is None:
                ttk.Label(self.info_frame, text="Vui lòng tải ảnh lên trước.").pack(anchor="w", pady=(6,0))
                return

            ops_frame = ttk.Frame(self.info_frame)
            ops_frame.pack(anchor="w", pady=(6,0))

            ttk.Label(ops_frame, text="Chọn phép:").grid(row=0, column=0, sticky="w")
            op_var = tk.StringVar(value="Âm bản")

            op_menu = ttk.Combobox(
                ops_frame, textvariable=op_var,
                values=["Âm bản", "Logarit", "Logarit ngược", "Gamma"],
                state="readonly", width=16
            )
            op_menu.grid(row=0, column=1, padx=(6,0))

            # Frame để chứa sliders (tự thay đổi khi chọn phép)
            slider_frame = ttk.Frame(self.info_frame)
            slider_frame.pack(anchor="w", pady=(6,0))

            # Các biến cần thiết
            c_var = tk.DoubleVar(value=1.0)
            base_var = tk.DoubleVar(value=2.718)
            gamma_var = tk.DoubleVar(value=1.0)

            # Hàm dựng sliders tương ứng phép
            def refresh_sliders(*args):
                for widget in slider_frame.winfo_children():
                    widget.destroy()

                sel = op_var.get()

                if sel == "Âm bản":
                    ttk.Label(slider_frame, text="Âm bản không cần tham số").pack(anchor="w")

                if sel in ["Logarit", "Logarit ngược"]:
                    ttk.Label(slider_frame, text="Hằng số c").pack(anchor="w")
                    tk.Scale(
                        slider_frame, variable=c_var,
                        from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
                        length=220
                    ).pack(anchor="w")

                    ttk.Label(slider_frame, text="Cơ số log").pack(anchor="w")
                    tk.Scale(
                        slider_frame, variable=base_var,
                        from_=1.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL,
                        length=220
                    ).pack(anchor="w")

                if sel == "Gamma":
                    ttk.Label(slider_frame, text="Gamma").pack(anchor="w")
                    tk.Scale(
                        slider_frame, variable=gamma_var,
                        from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
                        length=220
                    ).pack(anchor="w")

            # Update sliders mỗi khi đổi phép
            op_menu.bind("<<ComboboxSelected>>", refresh_sliders)
            refresh_sliders()

            # Nút áp dụng
            btn_frame = ttk.Frame(self.info_frame)
            btn_frame.pack(anchor="w", pady=(8,0))

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

            ttk.Button(btn_frame, text="Áp dụng", command=_map_and_apply).grid(row=0, column=0, padx=5)
            ttk.Button(btn_frame, text="Lưu kết quả...", command=self.save_processed).grid(row=0, column=1, padx=5)
            ttk.Button(btn_frame, text="Quay về ảnh gốc", command=lambda: self.show_image(self.original_image)).grid(row=0, column=2, padx=5)


    def apply_grayscale(self):
        if self.original_image is None:
            return None
        # Convert to L (grayscale) then back to RGBA for consistent display
        gray = self.original_image.convert("L").convert("RGBA")
        return gray

    def show_text(self, content: str):
        # hide canvas, show text widget
        try:
            self.canvas.pack_forget()
        except Exception:
            pass
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, content)
        self.text_widget.pack(fill="both", expand=True)

    # Metrics / matrix functions
    def compute_metrics_from_array(self, arr: np.ndarray):
        """Compute mean brightness, contrast (std), entropy, and sharpness (var of Laplacian)."""
        a = np.asarray(arr, dtype=float)
        # Độ sáng trung bình
        mean = float(np.mean(a))

        # Độ tương phản
        contrast = float(np.std(a))

        # Entropy
        vals = a.ravel()
        # Use integer bins when values are integers; otherwise quantize into 256 bins
        if np.issubdtype(a.dtype, np.integer) or np.all(np.mod(vals, 1) == 0):
            unique, counts = np.unique(vals, return_counts=True)
            probs = counts / counts.sum()
        else:
            counts, _ = np.histogram(vals, bins=256, range=(vals.min(), vals.max()))
            probs = counts / counts.sum()
        probs = probs[probs > 0]
        entropy = float(-(probs * np.log2(probs)).sum())

        # Độ sắc nét
        # Laplacian kernel
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
        pad = np.pad(a, pad_width=1, mode='edge')
        h, w = a.shape
        gx = np.zeros_like(a, dtype=float)
        gy = np.zeros_like(a, dtype=float)
        for y in range(h):
            for x in range(w):
                region = pad[y:y+3, x:x+3]
                gx[y, x] = np.sum(region * sobel_x)
                gy[y, x] = np.sum(region * sobel_y)
        grad_mag = np.sqrt(gx**2 + gy**2)
        sharpness = float(np.mean(grad_mag))

        return {
            'mean': mean,
            'contrast': contrast,
            'entropy': entropy,
            'sharpness': sharpness,
        }

    def format_metrics(self, name: str, metrics: dict):
        return (f"{name}:\n"
                f"  - Độ sáng trung bình: {metrics['mean']:.4f}\n"
                f"  - Độ tương phản (std): {metrics['contrast']:.4f}\n"
                f"  - Entropy: {metrics['entropy']:.6f}\n"
                f"  - Độ sắc nét (var Laplacian): {metrics['sharpness']:.6f}\n")

    def run_on_test_matrix(self):
        # Define M as in the prompt
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
        out = []
        out.append(self.format_metrics('Ma trận M (10x10)', m))
        self.show_text('\n'.join(out))

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

        # Using 1-based ranges from prompt: A = M(2:4,2:4) -> rows 1..3, cols 1..3
        A = M[1:4, 1:4]
        B = M[6:9, 1:4]  # M(7:9,2:4)
        C = M[1:4, 5:8]  # M(2:4,6:8)

        out_lines = []
        out_lines.append(self.format_metrics('Ma trận A (M[2:4,2:4])', self.compute_metrics_from_array(A)))
        out_lines.append(self.format_metrics('Ma trận B (M[7:9,2:4])', self.compute_metrics_from_array(B)))
        out_lines.append(self.format_metrics('Ma trận C (M[2:4,6:8])', self.compute_metrics_from_array(C)))

        self.show_text('\n'.join(out_lines))

    def run_on_loaded_image(self):
        if self.original_image is None:
            messagebox.showwarning('Chưa có ảnh', 'Vui lòng tải ảnh lên trước khi chạy trên ảnh.')
            return
        # convert to grayscale and extract matrix
        gray = self.original_image.convert('L')
        arr = np.array(gray, dtype=float)
        metrics = self.compute_metrics_from_array(arr)
        title = f"Ảnh: {self.current_filename} (grayscale)"
        self.show_text(self.format_metrics(title, metrics))

    # image transforms
    def apply_pixel_transform(self, op: str, c: float, base: float, gamma: float):
        if self.original_image is None:
            messagebox.showwarning('Chưa có ảnh', 'Vui lòng tải ảnh lên trước khi áp dụng biến đổi.')
            return

        img = self.original_image.convert("RGB")
        arr = np.array(img, dtype=float)  # shape (H, W, 3)

        out = np.zeros_like(arr)

    # Xử lý từng kênh màu độc lập
        for ch in range(3):
            r = arr[:, :, ch]

            if op == 'invert':
                s = 255.0 - r

            elif op == 'log':
                x = r / 255.0
                if base <= 0 or base == 1:
                    messagebox.showerror('Tham số không hợp lệ', 'Cơ số phải khác 1 và dương.')
                    return
                with np.errstate(divide='ignore'):
                    ln = np.log(1.0 + x)
                s = c * (ln / np.log(base))
                s = s - s.min()
                if s.max() > 0:
                    s = s / s.max()
                s = s * 255.0

            elif op == 'invlog' or op == 'inv-log' or op == 'inv_log':
                x = r / 255.0
                if base <= 0:
                    messagebox.showerror('Tham số không hợp lệ', 'Cơ số phải dương.')
                    return
                if c == 0:
                    messagebox.showerror('Tham số không hợp lệ', 'c không được bằng 0.')
                    return
                s = (base ** (x / c)) - 1.0
                s = s - s.min()
                if s.max() > 0:
                    s = s / s.max()
                s = s * 255.0

            elif op == 'gamma':
                x = r / 255.0
                with np.errstate(invalid='ignore'):
                    s = c * (x ** gamma)
                s = s * 255.0
            else:
                messagebox.showerror('Chức năng không hợp lệ', f'Phép không hợp lệ: {op}')
                return

            out[:, :, ch] = s

        # Clip and convert
        out = np.clip(out, 0, 255).astype(np.uint8)

        # Ghép alpha lại nếu có
        if self.has_alpha:
            alpha = np.array(self.original_image.split()[3])
            result_img = Image.fromarray(out, mode='RGB').convert("RGBA")
            result_img.putalpha(Image.fromarray(alpha))
        else:
            result_img = Image.fromarray(out, mode='RGB').convert("RGBA")
        self.processed_image = result_img
        self.show_image(self.processed_image)


    def show_image(self, pil_image):
        # If text widget visible, hide it
        try:
            self.text_widget.pack_forget()
        except Exception:
            pass
        # Resize to fit canvas while keeping aspect ratio
        self.canvas.pack(fill="both", expand=True)
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        img_w, img_h = pil_image.size
        ratio = min(w / img_w, h / img_h, 1.0)
        new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
        self.display_image = pil_image.resize(new_size, Image.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.create_image(w // 2, h // 2, image=self.photo_image, anchor="center")

    def save_processed(self):
        if self.processed_image is None:
            messagebox.showwarning("Không có ảnh xử lý", "Không có ảnh xử lý để lưu. Hãy chọn chức năng xử lý trước.")
            return
        filetypes = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("BMP", "*.bmp"),
            ("All files", "*.*"),
        ]
        initial = os.path.splitext(self.current_filename or "image")[0] + "_processed.png"
        path = filedialog.asksaveasfilename(title="Lưu ảnh xử lý", defaultextension=".png", filetypes=filetypes, initialfile=initial)
        if not path:
            return
        try:
            save_img = self.processed_image
            if os.path.splitext(path)[1].lower() in [".jpg", ".jpeg"]:
                save_img = save_img.convert("RGB")
            save_img.save(path)
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"Không thể lưu ảnh:\n{e}")
            return
        messagebox.showinfo("Hoàn tất", f"Đã lưu ảnh xử lý vào:\n{path}")

    def save_as(self):
        if self.original_image is None:
            messagebox.showwarning("Chưa có ảnh", "Vui lòng tải ảnh lên trước khi lưu.")
            return
        filetypes = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("BMP", "*.bmp"),
            ("All files", "*.*"),
        ]
        initial = os.path.splitext(self.current_filename or "image")[0] + ".png"
        path = filedialog.asksaveasfilename(title="Lưu ảnh dưới dạng", defaultextension=".png", filetypes=filetypes, initialfile=initial)
        if not path:
            return
        try:
            # Convert back to RGB for formats that don't support alpha
            save_img = self.original_image
            if os.path.splitext(path)[1].lower() in [".jpg", ".jpeg"]:
                save_img = save_img.convert("RGB")
            save_img.save(path)
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"Không thể lưu ảnh:\n{e}")
            return
        messagebox.showinfo("Hoàn tất", f"Đã lưu ảnh vào:\n{path}")


def main():
    app = ImageApp()
    app.mainloop()


if __name__ == "__main__":
    main()
