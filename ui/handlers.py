"""UI handlers cho các tính năng"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
import os

from features import grayscale, binary, red_channel, alpha, metrics, transform, contrast
from features import histogram_equalization


def create_save_ui(app, info_frame):
    """Tạo UI cho chức năng lưu ảnh"""
    title = tk.Label(info_frame, text="Lưu ảnh sang định dạng khác",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    desc = tk.Label(info_frame, 
                   text="Chọn định dạng mới để lưu ảnh gốc của bạn",
                   font=('Segoe UI', 9),
                   bg='white', fg='#7f8c8d')
    desc.pack(anchor='w', pady=(0, 15))
    
    save_btn = tk.Button(info_frame, text="Lưu ảnh...", 
                       command=app.save_as,
                       font=('Segoe UI', 10, 'bold'),
                       bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2',
                       padx=20, pady=10)
    save_btn.pack(anchor='w')


def create_grayscale_ui(app, info_frame):
    """Tạo UI cho chức năng chuyển ảnh xám"""
    title = tk.Label(info_frame, text="Chuyển ảnh xám",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return
    
    gray = grayscale.apply_grayscale(app.original_image)
    if gray is not None:
        app.processed_image = gray
        app.show_image(app.processed_image)
    
    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w', pady=(10, 0))
    
    save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                       command=app.save_processed,
                       font=('Segoe UI', 9), bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2', padx=15, pady=8)
    save_btn.grid(row=0, column=0, padx=(0, 10))
    
    revert_btn = tk.Button(btn_frame, text="Quay về ảnh gốc",
                         command=lambda: app.show_image(app.original_image),
                         font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                         relief='flat', cursor='hand2', padx=15, pady=8)
    revert_btn.grid(row=0, column=1)


def create_binary_ui(app, info_frame):
    """Tạo UI cho chức năng làm ảnh nhị phân"""
    title = tk.Label(info_frame, text="⬛ Làm ảnh nhị phân",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return
    
    base_gray = app.original_image.convert("L")
    
    slider_frame = tk.Frame(info_frame, bg='white')
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
        bw = binary.apply_binary(base_gray, t)
        app.processed_image = bw
        app.show_image(app.processed_image)

    slider.config(command=on_threshold)
    on_threshold(slider.get())

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w')
    
    save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                       command=app.save_processed,
                       font=('Segoe UI', 9), bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2', padx=15, pady=8)
    save_btn.grid(row=0, column=0, padx=(0, 10))
    
    revert_btn = tk.Button(btn_frame, text="Quay về ảnh gốc",
                         command=lambda: app.show_image(app.original_image),
                         font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                         relief='flat', cursor='hand2', padx=15, pady=8)
    revert_btn.grid(row=0, column=1)


def create_red_channel_ui(app, info_frame):
    """Tạo UI cho chức năng tách kênh đỏ"""
    title = tk.Label(info_frame, text="Tách kênh màu Đỏ",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return
    
    try:
        red_only = red_channel.extract_red(app.original_image)
        app.processed_image = red_only
        app.show_image(app.processed_image)
    except Exception as e:
        messagebox.showerror("Lỗi xử lý", f"Không thể tách kênh đỏ:\n{e}")
        return

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w', pady=(10, 0))
    
    save_btn = tk.Button(btn_frame, text="Lưu kết quả", 
                       command=app.save_processed,
                       font=('Segoe UI', 9), bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2', padx=15, pady=8)
    save_btn.grid(row=0, column=0, padx=(0, 10))
    
    revert_btn = tk.Button(btn_frame, text="↩️ Quay về ảnh gốc",
                         command=lambda: app.show_image(app.original_image),
                         font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                         relief='flat', cursor='hand2', padx=15, pady=8)
    revert_btn.grid(row=0, column=1)


def create_alpha_ui(app, info_frame):
    """Tạo UI cho chức năng kiểm tra kênh alpha"""
    title = tk.Label(info_frame, text="Kiểm tra kênh Alpha",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    alpha_img, info_text, _ = alpha.get_alpha_info(
        app.original_image, app.original_mode, app.has_alpha
    )
    
    if alpha_img is not None:
        app.processed_image = alpha_img
        app.show_image(app.processed_image)
    
    if info_text:
        app.show_text(info_text)


def create_metrics_ui(app, info_frame):
    """Tạo UI cho chức năng tính metrics"""
    title = tk.Label(info_frame, text="Tính 4 chỉ số",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 5))
    
    desc = tk.Label(info_frame, 
                   text="Độ sáng, Độ tương phản, Entropy, Độ sắc nét",
                   font=('Segoe UI', 9),
                   bg='white', fg='#7f8c8d')
    desc.pack(anchor='w', pady=(0, 15))
    
    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w')
    
    def run_on_test_matrix():
        M = metrics.get_test_matrix()
        m = metrics.compute_metrics_from_array(M)
        app.show_text(metrics.format_metrics("Ma trận M (10x10)", m))
    
    def run_on_submatrices():
        A, B, C = metrics.get_submatrices()
        text = ""
        text += metrics.format_metrics("Ma trận A", metrics.compute_metrics_from_array(A))
        text += "\n"
        text += metrics.format_metrics("Ma trận B", metrics.compute_metrics_from_array(B))
        text += "\n"
        text += metrics.format_metrics("Ma trận C", metrics.compute_metrics_from_array(C))
        app.show_text(text)
    
    def run_on_loaded_image():
        if app.original_image is None:
            messagebox.showwarning("Chưa có ảnh", "Hãy tải ảnh lên trước.")
            return
        import numpy as np
        gray = app.original_image.convert("L")
        arr = np.array(gray, float)
        m = metrics.compute_metrics_from_array(arr)
        app.show_text(metrics.format_metrics(f"Ảnh: {app.current_filename}", m))
    
    btns = [
        ("Ma trận M mẫu", run_on_test_matrix),
        ("Ma trận con A,B,C", run_on_submatrices),
        ("Ảnh đã tải", run_on_loaded_image)
    ]
    
    for i, (text, cmd) in enumerate(btns):
        btn = tk.Button(btn_frame, text=text, command=cmd,
                      font=('Segoe UI', 9), bg='#3498db', fg='white',
                      relief='flat', cursor='hand2', padx=15, pady=8)
        btn.grid(row=i, column=0, pady=5, sticky='ew')


def create_transform_ui(app, info_frame):
    """Tạo UI cho chức năng biến đổi ảnh"""
    title = tk.Label(info_frame, text="Biến đổi ảnh",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    ops_frame = tk.Frame(info_frame, bg='white')
    ops_frame.pack(anchor='w', pady=(0, 10), fill='x')

    tk.Label(ops_frame, text="Chọn phép biến đổi:",
            font=('Segoe UI', 9, 'bold'),
            bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
    
    op_var = tk.StringVar(value="Âm bản")
    op_menu = ttk.Combobox(ops_frame, textvariable=op_var,
                          values=["Âm bản", "Logarit", "Logarit ngược", "Gamma"],
                          state="readonly", width=20)
    op_menu.grid(row=0, column=1, padx=(10, 0), pady=5)

    slider_frame = tk.Frame(info_frame, bg='white')
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

    btn_frame = tk.Frame(info_frame, bg='white')
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
        result = transform.apply_pixel_transform(
            app.original_image, app.has_alpha, 
            op_code, c_var.get(), base_var.get(), gamma_var.get()
        )
        if result is not None:
            app.processed_image = result
            app.show_image(result)

    apply_btn = tk.Button(btn_frame, text="Áp dụng", command=_map_and_apply,
                        font=('Segoe UI', 9, 'bold'), bg='#3498db', fg='white',
                        relief='flat', cursor='hand2', padx=15, pady=8)
    apply_btn.grid(row=0, column=0, padx=(0, 10))
    
    save_btn = tk.Button(btn_frame, text="Lưu", command=app.save_processed,
                       font=('Segoe UI', 9), bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2', padx=15, pady=8)
    save_btn.grid(row=0, column=1, padx=(0, 10))
    
    revert_btn = tk.Button(btn_frame, text="Quay về", 
                         command=lambda: app.show_image(app.original_image),
                         font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                         relief='flat', cursor='hand2', padx=15, pady=8)
    revert_btn.grid(row=0, column=2)


def create_contrast_stretch_ui(app, info_frame):
    """Tạo UI cho chức năng kéo dãn độ tương phản"""
    title = tk.Label(info_frame, text="Kéo dãn độ tương phản",
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
            font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    # Frame chọn loại
    mode_var = tk.StringVar(value="linear")
    mode_frame = tk.Frame(info_frame, bg='white')
    mode_frame.pack(anchor='w')

    # Frame chứa sliders
    slider_frame = tk.Frame(info_frame, bg='white')
    slider_frame.pack(anchor='w', pady=10)

    # Các biến
    r_min_var = tk.IntVar(value=50)
    r_max_var = tk.IntVar(value=200)
    l0_var = tk.IntVar(value=50)
    l1_var = tk.IntVar(value=200)

    def apply_now(*args):
        result = contrast.apply_contrast_stretch(
            app.original_image,
            mode_var.get(),
            r_min_var.get(),
            r_max_var.get(),
            l0_var.get(),
            l1_var.get()
        )
        if result is not None:
            app.processed_image = result
            app.show_image(result)

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

    tk.Radiobutton(mode_frame, text="Loại 1 (Tuyến tính)", variable=mode_var,
                value="linear", bg='white',
                command=refresh_sliders).pack(anchor='w')

    tk.Radiobutton(mode_frame, text="Loại 2 (Từng phần)", variable=mode_var,
                value="piecewise", bg='white',
                command=refresh_sliders).pack(anchor='w')

    refresh_sliders()


def create_histogram_equalization_ui(app, info_frame):
    """Tạo UI cho chức năng cân bằng histogram"""
    title = tk.Label(info_frame, text="Cân bằng histogram tiêu chuẩn",
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh có độ tương phản thấp.",
            font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    # Kiểm tra xem ảnh là màu hay xám
    is_color = histogram_equalization.is_color_image(app.original_image)
    
    if is_color:
        # Ảnh màu: tách thành 3 kênh R, G, B
        r_matrix, g_matrix, b_matrix = histogram_equalization.get_color_channels(app.original_image)
        matrix = None
        display_image = app.original_image
    else:
        # Ảnh xám
        matrix = histogram_equalization.get_gray_matrix(app.original_image)
        r_matrix = g_matrix = b_matrix = None
        display_image = app.original_image.convert("L").convert("RGBA")
    
    if matrix is None and (r_matrix is None or g_matrix is None or b_matrix is None):
        messagebox.showerror("Lỗi", "Không thể xử lý ảnh")
        return

    # Frame chứa các nút
    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w', pady=(10, 0))

    def export_matrix():
        """Xuất ma trận ra file txt"""
        # Kiểm tra xem đã xử lý chưa
        if not hasattr(app, 'histogram_data'):
            messagebox.showwarning("Chưa xử lý", "Vui lòng thực hiện cân bằng histogram trước khi xuất ma trận.")
            return
            
        if is_color:
            # Xuất ma trận RGB sau khi xử lý vào 1 file
            if 'equalized_rgb' not in app.histogram_data:
                messagebox.showwarning("Chưa xử lý", "Vui lòng thực hiện cân bằng histogram trước.")
                return
                
            filename = filedialog.asksaveasfilename(
                title="Lưu ma trận RGB sau khi xử lý",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                r_eq, g_eq, b_eq = app.histogram_data['equalized_rgb']
                result = histogram_equalization.save_rgb_matrix_to_txt(r_eq, g_eq, b_eq, filename)
                if result:
                    messagebox.showinfo("Thành công", f"Đã lưu ma trận RGB vào:\n{filename}")
                else:
                    messagebox.showerror("Lỗi", "Không thể lưu file")
        else:
            filename = filedialog.asksaveasfilename(
                title="Lưu ma trận ảnh",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                # Xuất ma trận sau khi xử lý
                if hasattr(app, 'histogram_data') and 'equalized_matrix' in app.histogram_data:
                    eq_matrix = app.histogram_data['equalized_matrix']
                    result = histogram_equalization.save_matrix_to_txt(eq_matrix, filename, "sau xử lý")
                else:
                    result = histogram_equalization.save_matrix_to_txt(matrix, filename)
                if result:
                    messagebox.showinfo("Thành công", f"Đã lưu ma trận vào:\n{filename}")
                else:
                    messagebox.showerror("Lỗi", "Không thể lưu file")

    def process_equalization():
        """Thực hiện cân bằng histogram"""
        if is_color:
            # Xử lý ảnh màu: cân bằng từng kênh R, G, B
            h, w = r_matrix.shape
            total_pixels = h * w

            # Xử lý kênh R
            r_nk = histogram_equalization.step1_count_pixels(r_matrix)
            r_cdf = histogram_equalization.step2_calculate_cdf(r_nk, total_pixels)
            r_sk = histogram_equalization.step3_calculate_output_levels(r_cdf)
            r_nk_new = histogram_equalization.step4_count_output_pixels(r_nk, r_sk)
            r_results = histogram_equalization.format_step_results(r_nk, r_cdf, r_sk, r_nk_new, total_pixels, "R")

            # Xử lý kênh G
            g_nk = histogram_equalization.step1_count_pixels(g_matrix)
            g_cdf = histogram_equalization.step2_calculate_cdf(g_nk, total_pixels)
            g_sk = histogram_equalization.step3_calculate_output_levels(g_cdf)
            g_nk_new = histogram_equalization.step4_count_output_pixels(g_nk, g_sk)
            g_results = histogram_equalization.format_step_results(g_nk, g_cdf, g_sk, g_nk_new, total_pixels, "G")

            # Xử lý kênh B
            b_nk = histogram_equalization.step1_count_pixels(b_matrix)
            b_cdf = histogram_equalization.step2_calculate_cdf(b_nk, total_pixels)
            b_sk = histogram_equalization.step3_calculate_output_levels(b_cdf)
            b_nk_new = histogram_equalization.step4_count_output_pixels(b_nk, b_sk)
            b_results = histogram_equalization.format_step_results(b_nk, b_cdf, b_sk, b_nk_new, total_pixels, "B")

            # Tạo ảnh mới
            equalized_img, r_eq_matrix, g_eq_matrix, b_eq_matrix = histogram_equalization.step5_create_equalized_color_image(
                r_matrix, g_matrix, b_matrix, r_sk, g_sk, b_sk
            )

            # Lưu kết quả vào app
            app.processed_image = equalized_img
            app.histogram_data = {
                'is_color': True,
                'original': {'R': r_nk, 'G': g_nk, 'B': b_nk},
                'equalized': {'R': r_nk_new, 'G': g_nk_new, 'B': b_nk_new},
                'equalized_rgb': (r_eq_matrix, g_eq_matrix, b_eq_matrix),
                'steps_text': histogram_equalization.format_color_step_results(r_results, g_results, b_results)
            }
        else:
            # Xử lý ảnh xám
            h, w = matrix.shape
            total_pixels = h * w

            # Bước 1: Thống kê số lượng pixel
            nk = histogram_equalization.step1_count_pixels(matrix)

            # Bước 2: Tính CDF
            cdf = histogram_equalization.step2_calculate_cdf(nk, total_pixels)

            # Bước 3: Tính mức xám đầu ra
            sk = histogram_equalization.step3_calculate_output_levels(cdf)

            # Bước 4: Tính số lượng pixel mới
            nk_new = histogram_equalization.step4_count_output_pixels(nk, sk)

            # Bước 5: Tạo ảnh mới
            equalized_img = histogram_equalization.step5_create_equalized_image(matrix, sk)

            # Lưu kết quả vào app
            app.processed_image = equalized_img
            app.histogram_data = {
                'is_color': False,
                'original': nk,
                'equalized': nk_new,
                'matrix': matrix,
                'equalized_matrix': np.array(equalized_img.convert("L")),
                'steps_text': histogram_equalization.format_step_results(nk, cdf, sk, nk_new, total_pixels)
            }

        # Hiển thị kết quả
        show_results()

    def show_results():
        """Hiển thị kết quả và so sánh"""
        if not hasattr(app, 'histogram_data'):
            return

        data = app.histogram_data
        
        # Xóa các widget cũ trong info_frame (trừ title và btn_frame)
        for widget in info_frame.winfo_children():
            if widget != title and widget != btn_frame:
                widget.destroy()
        

        # Đặt đoạn này ở đầu file hoặc trong class App (tùy cấu trúc của bạn)

        def create_scrollable_area(parent_frame):
            """Tạo Canvas và Scrollbar, trả về Frame bên trong để chứa nội dung."""
            # Tạo Canvas
            canvas = tk.Canvas(parent_frame, bg='white', highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            # Tạo Scrollbar
            scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            # Kết nối Canvas với Scrollbar
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Tạo Frame chứa nội dung bên trong Canvas
            scrollable_frame = tk.Frame(canvas, bg='white')
            
            # Đặt Frame vào Canvas
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Thiết lập vùng cuộn khi Frame thay đổi kích thước
            # Điều này quan trọng để Canvas biết tổng chiều cao của nội dung
            def on_frame_configure(event):
                # Tính lại scrollregion (vùng cuộn) dựa trên kích thước của scrollable_frame
                canvas.configure(scrollregion=canvas.bbox("all"))

            scrollable_frame.bind("<Configure>", on_frame_configure)
            
            canvas.bind_all("<MouseWheel>", 
                            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

            return scrollable_frame, canvas

        scroll_container = tk.Frame(info_frame, bg='white')
        scroll_container.pack(fill='both', expand=True, pady=(10, 0))

        # Khởi tạo khu vực cuộn
        scrollable_content_frame, canvas_widget = create_scrollable_area(scroll_container)
        content_frame = scrollable_content_frame

        # Hiển thị ảnh
        images_frame = tk.Frame(content_frame, bg='white')
        images_frame.pack(fill='x', pady=(0, 15))
        
        # Label cho phần ảnh
        images_label = tk.Label(images_frame, text="So sánh ảnh trước và sau cân bằng:",
                               font=('Segoe UI', 11, 'bold'), bg='white', fg='#2c3e50')
        images_label.pack(anchor='w', pady=(0, 10))
        
        # Frame chứa 2 ảnh cạnh nhau
        images_container = tk.Frame(images_frame, bg='white')
        images_container.pack(fill='x')
        
        # Ảnh gốc
        orig_frame = tk.Frame(images_container, bg='#ecf0f1', relief='flat', padx=5, pady=5)
        orig_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        orig_label = tk.Label(orig_frame, text="Ảnh gốc", 
                             font=('Segoe UI', 9, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        orig_label.pack(pady=(0, 5))
        
        orig_canvas = tk.Canvas(orig_frame, width=300, height=300, bg='white', 
                                highlightthickness=1, highlightbackground='#bdc3c7')
        orig_canvas.pack()
        
        # Resize và hiển thị ảnh gốc (giữ tỷ lệ)
        def resize_keep_ratio(img, max_size):
            """Resize ảnh giữ tỷ lệ khung hình"""
            w, h = img.size
            ratio = min(max_size[0] / w, max_size[1] / h, 1.0)
            new_size = (int(w * ratio), int(h * ratio))
            return img.resize(new_size, Image.LANCZOS)
        
        orig_img_resized = resize_keep_ratio(display_image, (300, 300))
        orig_photo = ImageTk.PhotoImage(orig_img_resized)
        orig_canvas.create_image(150, 150, image=orig_photo, anchor="center")
        orig_canvas.image = orig_photo  # Giữ reference
        
        # Ảnh sau cân bằng
        eq_frame = tk.Frame(images_container, bg='#ecf0f1', relief='flat', padx=5, pady=5)
        eq_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        eq_label = tk.Label(eq_frame, text="Ảnh sau cân bằng", 
                           font=('Segoe UI', 9, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        eq_label.pack(pady=(0, 5))
        
        eq_canvas = tk.Canvas(eq_frame, width=300, height=300, bg='white',
                             highlightthickness=1, highlightbackground='#bdc3c7')
        eq_canvas.pack()
        
        # Resize và hiển thị ảnh sau cân bằng (giữ tỷ lệ)
        eq_img_resized = resize_keep_ratio(app.processed_image, (300, 300))
        eq_photo = ImageTk.PhotoImage(eq_img_resized)
        eq_canvas.create_image(150, 150, image=eq_photo, anchor="center")
        eq_canvas.image = eq_photo  # Giữ reference
        
        # Hiển thị Histogram
        hist_frame = tk.Frame(content_frame, bg='white')
        hist_frame.pack(fill='x', pady=(0, 15))
        
        hist_label = tk.Label(hist_frame, text="So sánh histogram:",
                             font=('Segoe UI', 11, 'bold'), bg='white', fg='#2c3e50')
        hist_label.pack(anchor='w', pady=(0, 10))
        
        if data.get('is_color', False):
            # Hiển thị histogram ảnh màu trên 6 canvas (3 Gốc & 3 Sau cân bằng)
            canvas_width = 300 # Giảm chiều rộng để có thể đặt cạnh nhau
            canvas_height = 180
            
            # Tạo frame chứa 6 canvas theo lưới 2x3
            hist_container = tk.Frame(hist_frame, bg='white')
            hist_container.pack(fill='x', expand=True)

            channels = [('R', '#e74c3c', '#c0392b'), 
                        ('G', '#27ae60', '#229954'), 
                        ('B', '#3498db', '#2980b9')]
            
            # Label hướng dẫn
            tk.Label(hist_container, text="Ảnh Gốc", font=('Segoe UI', 9, 'bold'), bg='white', fg='#c0392b').grid(row=0, column=0, padx=5)
            tk.Label(hist_container, text="Ảnh Sau Cân Bằng", font=('Segoe UI', 9, 'bold'), bg='white', fg='#229954').grid(row=0, column=1, padx=5)
            
            for i, (channel_name, orig_color, eq_color) in enumerate(channels):
                # Tiêu đề kênh màu
                tk.Label(hist_container, text=f"Kênh {channel_name}", font=('Segoe UI', 9), bg='white', fg='#2c3e50').grid(row=i+1, column=0, columnspan=2, pady=(10,0))
                
                # Canvas cho Ảnh Gốc (kênh i)
                orig_canvas = tk.Canvas(
                    hist_container,
                    width=canvas_width, height=canvas_height, bg='white',
                    highlightthickness=1, highlightbackground='#bdc3c7'
                )
                orig_canvas.grid(row=i+2, column=0, padx=5, pady=5)
                draw_histogram(orig_canvas, data['original'][channel_name], 0, 0,
                               canvas_width, canvas_height, f"Gốc - Kênh {channel_name}", orig_color)
                
                # Canvas cho Ảnh Sau Cân Bằng (kênh i)
                eq_canvas = tk.Canvas(
                    hist_container,
                    width=canvas_width, height=canvas_height, bg='white',
                    highlightthickness=1, highlightbackground='#bdc3c7'
                )
                eq_canvas.grid(row=i+2, column=1, padx=5, pady=5)
                draw_histogram(eq_canvas, data['equalized'][channel_name], 0, 0,
                               canvas_width, canvas_height, f"Sau cân bằng - Kênh {channel_name}", eq_color)
        else:
            # Hiển thị histogram cho ảnh xám
            canvas_width = 600
            canvas_height = 200
            
            hist_canvas = tk.Canvas(hist_frame, width=canvas_width, height=canvas_height * 2 + 40,
                                   bg='white', highlightthickness=1, highlightbackground='#bdc3c7')
            hist_canvas.pack(pady=10)

            # Vẽ histogram ảnh gốc
            draw_histogram(hist_canvas, data['original'], 0, 0, canvas_width, canvas_height, 
                          "Histogram ảnh gốc", '#3498db')
            
            # Vẽ histogram ảnh sau cân bằng
            draw_histogram(hist_canvas, data['equalized'], 0, canvas_height + 20, 
                          canvas_width, canvas_height, "Histogram sau cân bằng", '#27ae60')
        
        # Phân tích kết quả
        analysis_frame = tk.Frame(content_frame, bg='white')
        analysis_frame.pack(fill='x', pady=(0, 10))
        
        analysis_label = tk.Label(analysis_frame, text="Phân tích kết quả:",
                                 font=('Segoe UI', 11, 'bold'), bg='white', fg='#2c3e50')
        analysis_label.pack(anchor='w', pady=(0, 5))
        
        # Tính toán các chỉ số
        if data.get('is_color', False):
            # Tính cho từng kênh màu
            r_orig_levels = np.count_nonzero(data['original']['R'])
            r_eq_levels = np.count_nonzero(data['equalized']['R'])
            g_orig_levels = np.count_nonzero(data['original']['G'])
            g_eq_levels = np.count_nonzero(data['equalized']['G'])
            b_orig_levels = np.count_nonzero(data['original']['B'])
            b_eq_levels = np.count_nonzero(data['equalized']['B'])
            
            analysis_text = f"""
• Số mức xám được sử dụng (từng kênh):
  - Kênh R: {r_orig_levels} → {r_eq_levels} mức (tăng {r_eq_levels - r_orig_levels})
  - Kênh G: {g_orig_levels} → {g_eq_levels} mức (tăng {g_eq_levels - g_orig_levels})
  - Kênh B: {b_orig_levels} → {b_eq_levels} mức (tăng {b_eq_levels - b_orig_levels})

• Kết luận:
  Cân bằng histogram đã được thực hiện độc lập cho từng kênh màu R, G, B.
  Điều này giúp cải thiện độ tương phản và phân bố màu sắc của ảnh một cách tự nhiên.
            """
        else:
            orig_used_levels = np.count_nonzero(data['original'])
            eq_used_levels = np.count_nonzero(data['equalized'])
            orig_std = np.std(data['original'])
            eq_std = np.std(data['equalized'])
            
            analysis_text = f"""
• Số mức xám được sử dụng:
  - Trước cân bằng: {orig_used_levels} mức
  - Sau cân bằng: {eq_used_levels} mức
  - Cải thiện: {'Có' if eq_used_levels > orig_used_levels else 'Không'} (tăng {eq_used_levels - orig_used_levels} mức)

• Độ phân tán histogram:
  - Trước cân bằng: {orig_std:.2f}
  - Sau cân bằng: {eq_std:.2f}
  - Đánh giá: {'Histogram được phân bố đều hơn' if eq_std < orig_std else 'Histogram phân tán hơn'}

• Kết luận:
  Cân bằng histogram đã {'cải thiện' if eq_used_levels > orig_used_levels else 'không cải thiện'} 
  việc phân bố mức xám, giúp ảnh có độ tương phản tốt hơn và chi tiết rõ ràng hơn.
            """
        
        analysis_widget = tk.Text(analysis_frame, font=('Segoe UI', 9),
                                 bg='#f8f9fa', fg='#2c3e50',
                                 relief='flat', padx=10, pady=10, height=8, wrap='word')
        analysis_widget.insert("1.0", analysis_text.strip())
        analysis_widget.config(state='disabled')
        analysis_widget.pack(fill='x')
        
        details_frame = tk.Frame(content_frame, bg='white')
        details_frame.pack(fill='both', expand=True)
        
        # Tạo frame có thể thu gọn
        details_header = tk.Frame(details_frame, bg='#ecf0f1', relief='flat')
        details_header.pack(fill='x')
        
        details_label = tk.Label(details_header, text="📋 Chi tiết các bước xử lý (click để mở/đóng)",
                                font=('Segoe UI', 10, 'bold'), bg='#ecf0f1', fg='#2c3e50', cursor='hand2')
        details_label.pack(side='left', padx=10, pady=5)
        
        details_text_frame = tk.Frame(details_frame, bg='white')
        details_text_frame.pack_forget()  # Ẩn ban đầu
        
        text_widget = tk.Text(details_text_frame, font=('Consolas', 8),
                             bg='#2c3e50', fg='#ecf0f1',
                             relief='flat', padx=10, pady=10, height=12, wrap='none')
        text_scrollbar = tk.Scrollbar(details_text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=text_scrollbar.set)
        text_widget.insert("1.0", data['steps_text'])
        text_widget.config(state='disabled')
        text_widget.pack(side='left', fill='both', expand=True)
        text_scrollbar.pack(side='right', fill='y')
        
        def toggle_details():
            if details_text_frame.winfo_viewable():
                details_text_frame.pack_forget()
            else:
                details_text_frame.pack(fill='both', expand=True)
        
        details_label.bind('<Button-1>', lambda e: toggle_details())
        
        # Nút điều khiển
        view_btn_frame = tk.Frame(info_frame, bg='white')
        view_btn_frame.pack(anchor='w', pady=(10, 0))

        view_orig_btn = tk.Button(view_btn_frame, text="🔍 Xem ảnh gốc (full size)",
                                 command=lambda: app.show_image(display_image),
                                 font=('Segoe UI', 9), bg='#3498db', fg='white',
                                 relief='flat', cursor='hand2', padx=15, pady=8)
        view_orig_btn.grid(row=0, column=0, padx=(0, 10))

        view_eq_btn = tk.Button(view_btn_frame, text="🔍 Xem ảnh sau cân bằng (full size)",
                               command=lambda: app.show_image(app.processed_image),
                               font=('Segoe UI', 9), bg='#27ae60', fg='white',
                               relief='flat', cursor='hand2', padx=15, pady=8)
        view_eq_btn.grid(row=0, column=1, padx=(0, 10))

        save_btn = tk.Button(view_btn_frame, text="💾 Lưu ảnh sau cân bằng",
                            command=app.save_processed,
                            font=('Segoe UI', 9), bg='#27ae60', fg='white',
                            relief='flat', cursor='hand2', padx=15, pady=8)
        save_btn.grid(row=0, column=2)

    def draw_histogram(canvas, nk, x_offset, y_offset, width, height, title, color):
        """Vẽ histogram trên canvas"""
        if nk is None or len(nk) == 0:
            return

        max_count = np.max(nk)
        if max_count == 0:
            return

        # Vẽ tiêu đề
        canvas.create_text(x_offset + width // 2, y_offset + 15, 
                         text=title, font=('Segoe UI', 10, 'bold'), fill='#2c3e50')

        # Vẽ trục (đặt trục X gần đáy canvas để histogram không bị dồn lên trên)
        margin_left = 40
        margin_bottom = 30
        margin_right = 20
        margin_top = 20

        chart_x = x_offset + margin_left
        chart_y = y_offset + height - margin_bottom   # trục X gần đáy
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom

        # Vẽ trục X và Y
        canvas.create_line(chart_x, chart_y, chart_x + chart_width, chart_y, fill='#34495e', width=2)
        canvas.create_line(chart_x, chart_y, chart_x, chart_y - chart_height, fill='#34495e', width=2)

        # Vẽ nhãn trục
        canvas.create_text(chart_x - 20, chart_y - chart_height // 2, 
                         text="Số\nlượng", font=('Segoe UI', 8), fill='#7f8c8d', angle=90)
        canvas.create_text(chart_x + chart_width // 2, chart_y + 20, 
                         text="Mức xám (0-255)", font=('Segoe UI', 8), fill='#7f8c8d')

        # Vẽ các cột histogram
        bar_width = chart_width / 256
        for k in range(256):
            if nk[k] > 0:
                bar_height = (nk[k] / max_count) * chart_height
                x1 = chart_x + k * bar_width
                y1 = chart_y
                x2 = x1 + bar_width
                y2 = chart_y - bar_height
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

        # Vẽ giá trị max
        canvas.create_text(chart_x - 10, chart_y - chart_height, 
                         text=str(int(max_count)), font=('Segoe UI', 7), fill='#7f8c8d', anchor='e')
        canvas.create_text(chart_x - 10, chart_y, 
                         text="0", font=('Segoe UI', 7), fill='#7f8c8d', anchor='e')

    # Các nút điều khiển
    export_btn = tk.Button(btn_frame, text="📄 Xuất ma trận ra file txt",
                          command=export_matrix,
                          font=('Segoe UI', 9), bg='#3498db', fg='white',
                          relief='flat', cursor='hand2', padx=15, pady=8)
    export_btn.grid(row=0, column=0, padx=(0, 10))

    process_btn = tk.Button(btn_frame, text="⚙️ Thực hiện cân bằng histogram",
                           command=process_equalization,
                           font=('Segoe UI', 9, 'bold'), bg='#27ae60', fg='white',
                           relief='flat', cursor='hand2', padx=15, pady=8)
    process_btn.grid(row=0, column=1)

    # Hiển thị ảnh gốc
    app.show_image(display_image)

