"""UI handlers cho các tính năng"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
import os

from features import grayscale, binary, red_channel, alpha, metrics, transform, contrast
from features import histogram_equalization, histogram_matching, adaptive_histogram, convolution, noise
from utils.image_utils import resize_for_display


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


# === Histogram Matching ===

def create_histogram_matching_ui(app, info_frame):
    """UI cho Histogram Matching"""
    title = tk.Label(info_frame, text="Histogram Matching",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    if app.original_image is None:
        tk.Label(info_frame, text="Vui long tai anh nguon truoc.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    state = {"ref_img": None, "matched_img": None, "photos": []}

    desc = tk.Label(
        info_frame,
        text="Chon anh tham chieu, thuc hien matching, hien thi 3 anh va histogram.",
        font=('Segoe UI', 9),
        bg='white',
        fg='#7f8c8d',
        justify='left'
    )
    desc.pack(anchor='w', pady=(0, 10))

    control_frame = tk.Frame(info_frame, bg='white')
    control_frame.pack(anchor='w', pady=(0, 10), fill='x')

    ref_label = tk.Label(control_frame, text="Chua chon anh tham chieu",
                        font=('Segoe UI', 9), bg='white', fg='#7f8c8d')
    ref_label.grid(row=0, column=0, sticky='w')

    def load_reference():
        path = filedialog.askopenfilename(
            title="Chon anh tham chieu",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            img = Image.open(path).convert("RGBA")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong mo duoc anh tham chieu:\n{e}")
            return
        state["ref_img"] = img
        ref_label.config(text=f"Tham chieu: {os.path.basename(path)}", fg='#2ecc71')
        refresh_previews()

    load_ref_btn = tk.Button(control_frame, text="Chon anh tham chieu",
                            command=load_reference,
                            font=('Segoe UI', 9), bg='#3498db', fg='white',
                            relief='flat', cursor='hand2', padx=12, pady=8)
    load_ref_btn.grid(row=0, column=1, padx=(10, 0))

    run_btn = tk.Button(control_frame, text="Thuc hien matching",
                       command=lambda: process_matching(),
                       font=('Segoe UI', 9, 'bold'), bg='#27ae60', fg='white',
                       relief='flat', cursor='hand2', padx=12, pady=8)
    run_btn.grid(row=0, column=2, padx=(10, 0))

    save_btn = tk.Button(control_frame, text="Luu ket qua",
                        command=app.save_processed,
                        font=('Segoe UI', 9), bg='#27ae60', fg='white',
                        relief='flat', cursor='hand2', padx=12, pady=8)
    save_btn.grid(row=0, column=3, padx=(10, 0))

    revert_btn = tk.Button(control_frame, text="Quay ve anh goc",
                          command=lambda: app.show_image(app.original_image),
                          font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                          relief='flat', cursor='hand2', padx=12, pady=8)
    revert_btn.grid(row=0, column=4, padx=(10, 0))

    preview_frame = tk.Frame(info_frame, bg='white')
    preview_frame.pack(fill='x', pady=(5, 0))

    img_frame = tk.Frame(preview_frame, bg='white')
    img_frame.pack(fill='x')

    hist_frame = tk.Frame(preview_frame, bg='white')
    hist_frame.pack(fill='x', pady=(10, 0))

    canvases = {}
    hist_canvases = {}
    labels = ["Nguon", "Tham chieu", "Ket qua"]
    for idx, name in enumerate(labels):
        wrapper = tk.Frame(img_frame, bg='white')
        wrapper.grid(row=0, column=idx, padx=5)
        tk.Label(wrapper, text=name, font=('Segoe UI', 9, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        c = tk.Canvas(wrapper, width=230, height=150, bg='#ecf0f1',
                     highlightthickness=1, highlightbackground='#bdc3c7')
        c.pack()
        canvases[name] = c

        hist_wrap = tk.Frame(hist_frame, bg='white')
        hist_wrap.grid(row=0, column=idx, padx=5)
        tk.Label(hist_wrap, text=f"Histogram {name}", font=('Segoe UI', 9),
                bg='white', fg='#2c3e50').pack(anchor='w')
        hc = tk.Canvas(hist_wrap, width=230, height=140, bg='white',
                      highlightthickness=1, highlightbackground='#bdc3c7')
        hc.pack()
        hist_canvases[name] = hc

    summary = tk.Label(info_frame, text="", font=('Segoe UI', 9),
                      bg='white', fg='#2c3e50', justify='left')
    summary.pack(anchor='w', pady=(8, 0))

    def compute_histogram(pil_img):
        if pil_img is None:
            return None
        arr = np.array(pil_img.convert("L"))
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        return hist

    def draw_hist(canvas, hist, color="#3498db"):
        canvas.delete("all")
        if hist is None:
            canvas.create_text(115, 70, text="Khong co du lieu",
                             font=('Segoe UI', 9), fill='#7f8c8d')
            return
        max_val = np.max(hist) if len(hist) else 0
        if max_val == 0:
            return
        w = 230
        h = 140
        margin = 20
        chart_w = w - margin * 2
        chart_h = h - margin * 2
        for i in range(256):
            if hist[i] == 0:
                continue
            x0 = margin + (i / 256.0) * chart_w
            x1 = margin + ((i + 1) / 256.0) * chart_w
            bar_h = (hist[i] / max_val) * chart_h
            y0 = h - margin
            y1 = y0 - bar_h
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def show_image_on_canvas(canvas, pil_img):
        canvas.delete("all")
        if pil_img is None:
            canvas.create_text(115, 75, text="Khong co anh",
                             font=('Segoe UI', 9), fill='#7f8c8d')
            return
        img = pil_img.convert("RGB").copy()
        img.thumbnail((220, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        state["photos"].append(photo)
        canvas.create_image(115, 75, image=photo)

    def refresh_previews():
        state["photos"].clear()
        src_img = app.original_image
        ref_img = state["ref_img"]
        matched_img = state["matched_img"]

        show_image_on_canvas(canvases["Nguon"], src_img)
        draw_hist(hist_canvases["Nguon"], compute_histogram(src_img))

        show_image_on_canvas(canvases["Tham chieu"], ref_img)
        draw_hist(hist_canvases["Tham chieu"], compute_histogram(ref_img))

        show_image_on_canvas(canvases["Ket qua"], matched_img)
        draw_hist(hist_canvases["Ket qua"], compute_histogram(matched_img))

    def process_matching():
        if state["ref_img"] is None:
            messagebox.showwarning("Thieu tham chieu", "Vui long chon anh tham chieu truoc.")
            return
        try:
            matched = histogram_matching.histogram_matching(app.original_image, state["ref_img"])
            matched_rgba = matched.convert("RGBA")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong thuc hien matching:\n{e}")
            return

        state["matched_img"] = matched_rgba
        app.processed_image = matched_rgba
        app.show_image(matched_rgba)
        refresh_previews()

        summary.config(text="Da khop histogram nguon sang tham chieu. Quan sat histogram 3 anh de so sanh.")

    refresh_previews()
    app.show_image(app.original_image)


# === Adaptive Histogram Equalization ===

def create_adaptive_histogram_ui(app, info_frame):
    """UI cho Adaptive Histogram Equalization"""
    title = tk.Label(info_frame, text="Adaptive Histogram Equalization",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    if app.original_image is None:
        tk.Label(info_frame, text="Vui long tai anh truoc.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    state = {"global_img": None, "local_img": None, "photos": []}

    desc = tk.Label(
        info_frame,
        text="So sanh can bang histogram toan cuc va can bang cuc bo (adaptive).",
        font=('Segoe UI', 9),
        bg='white',
        fg='#7f8c8d',
        justify='left'
    )
    desc.pack(anchor='w', pady=(0, 10))

    tile_frame = tk.Frame(info_frame, bg='white')
    tile_frame.pack(anchor='w', pady=(0, 10))
    tk.Label(tile_frame, text="Tile size:", font=('Segoe UI', 9, 'bold'),
            bg='white', fg='#2c3e50').grid(row=0, column=0, padx=(0, 8))
    tile_var = tk.IntVar(value=32)
    tk.Scale(tile_frame, from_=8, to=64, orient=tk.HORIZONTAL,
            variable=tile_var, resolution=4, length=250,
            bg='white', highlightthickness=0,
            troughcolor='#ecf0f1').grid(row=0, column=1, padx=(0, 10))

    tk.Button(tile_frame, text="Thuc hien",
             command=lambda: process_adaptive(),
             font=('Segoe UI', 9, 'bold'), bg='#27ae60', fg='white',
             relief='flat', cursor='hand2', padx=12, pady=8).grid(row=0, column=2)

    tk.Button(tile_frame, text="Xem anh goc",
             command=lambda: app.show_image(app.original_image),
             font=('Segoe UI', 9), bg='#3498db', fg='white',
             relief='flat', cursor='hand2', padx=12, pady=8).grid(row=0, column=3, padx=(10, 0))

    preview_frame = tk.Frame(info_frame, bg='white')
    preview_frame.pack(fill='x')

    img_frame = tk.Frame(preview_frame, bg='white')
    img_frame.pack(fill='x')

    hist_frame = tk.Frame(preview_frame, bg='white')
    hist_frame.pack(fill='x', pady=(10, 0))

    canvases = {}
    hist_canvases = {}
    labels = [("Goc", "#2980b9"), ("Toan cuc", "#27ae60"), ("Adaptive", "#e67e22")]
    for idx, (name, _) in enumerate(labels):
        wrapper = tk.Frame(img_frame, bg='white')
        wrapper.grid(row=0, column=idx, padx=5)
        tk.Label(wrapper, text=name, font=('Segoe UI', 9, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        c = tk.Canvas(wrapper, width=230, height=150, bg='#ecf0f1',
                     highlightthickness=1, highlightbackground='#bdc3c7')
        c.pack()
        canvases[name] = c

        hist_wrap = tk.Frame(hist_frame, bg='white')
        hist_wrap.grid(row=0, column=idx, padx=5)
        tk.Label(hist_wrap, text=f"Histogram {name}", font=('Segoe UI', 9),
                bg='white', fg='#2c3e50').pack(anchor='w')
        hc = tk.Canvas(hist_wrap, width=230, height=140, bg='white',
                      highlightthickness=1, highlightbackground='#bdc3c7')
        hc.pack()
        hist_canvases[name] = hc

    analysis_text = tk.Text(info_frame, font=('Segoe UI', 9),
                           bg='#f8f9fa', fg='#2c3e50',
                           relief='flat', height=5, wrap='word')
    analysis_text.pack(fill='x', pady=(10, 0))
    analysis_text.insert("1.0", "Nhan 'Thuc hien' de so sanh.")
    analysis_text.config(state='disabled')

    def compute_histogram(pil_img):
        if pil_img is None:
            return None
        arr = np.array(pil_img.convert("L"))
        hist, _ = np.histogram(arr.flatten(), bins=256, range=[0, 256])
        return hist

    def draw_hist(canvas, hist, color="#3498db"):
        canvas.delete("all")
        if hist is None:
            canvas.create_text(115, 70, text="Khong co du lieu",
                             font=('Segoe UI', 9), fill='#7f8c8d')
            return
        max_val = np.max(hist) if len(hist) else 0
        if max_val == 0:
            return
        w = 230
        h = 140
        margin = 20
        chart_w = w - margin * 2
        chart_h = h - margin * 2
        for i in range(256):
            if hist[i] == 0:
                continue
            x0 = margin + (i / 256.0) * chart_w
            x1 = margin + ((i + 1) / 256.0) * chart_w
            bar_h = (hist[i] / max_val) * chart_h
            y0 = h - margin
            y1 = y0 - bar_h
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def show_image_on_canvas(canvas, pil_img):
        canvas.delete("all")
        if pil_img is None:
            canvas.create_text(115, 75, text="Khong co anh",
                             font=('Segoe UI', 9), fill='#7f8c8d')
            return
        img = pil_img.convert("RGB").copy()
        img.thumbnail((220, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        state["photos"].append(photo)
        canvas.create_image(115, 75, image=photo)

    def refresh_previews():
        state["photos"].clear()
        show_image_on_canvas(canvases["Goc"], app.original_image)
        draw_hist(hist_canvases["Goc"], compute_histogram(app.original_image), labels[0][1])

        show_image_on_canvas(canvases["Toan cuc"], state["global_img"])
        draw_hist(hist_canvases["Toan cuc"], compute_histogram(state["global_img"]) if state["global_img"] else None, labels[1][1])

        show_image_on_canvas(canvases["Adaptive"], state["local_img"])
        draw_hist(hist_canvases["Adaptive"], compute_histogram(state["local_img"]) if state["local_img"] else None, labels[2][1])

    def process_adaptive():
        try:
            if histogram_equalization.is_color_image(app.original_image):
                r_matrix, g_matrix, b_matrix = histogram_equalization.get_color_channels(app.original_image)
                total_pixels = r_matrix.size

                def eq_channel(mat):
                    nk = histogram_equalization.step1_count_pixels(mat)
                    cdf = histogram_equalization.step2_calculate_cdf(nk, total_pixels)
                    sk = histogram_equalization.step3_calculate_output_levels(cdf)
                    histogram_equalization.step4_count_output_pixels(nk, sk)
                    return sk

                r_sk = eq_channel(r_matrix)
                g_sk = eq_channel(g_matrix)
                b_sk = eq_channel(b_matrix)
                global_img, _, _, _ = histogram_equalization.step5_create_equalized_color_image(
                    r_matrix, g_matrix, b_matrix, r_sk, g_sk, b_sk
                )
            else:
                gray_matrix = histogram_equalization.get_gray_matrix(app.original_image)
                total_pixels = gray_matrix.size
                nk = histogram_equalization.step1_count_pixels(gray_matrix)
                cdf = histogram_equalization.step2_calculate_cdf(nk, total_pixels)
                sk = histogram_equalization.step3_calculate_output_levels(cdf)
                histogram_equalization.step4_count_output_pixels(nk, sk)
                global_img = histogram_equalization.step5_create_equalized_image(gray_matrix, sk)

            local_img = adaptive_histogram.adaptive_histogram_equalization(
                app.original_image, tile_size=tile_var.get()
            )
            if local_img.mode != "RGBA":
                local_img = local_img.convert("RGBA")

            state["global_img"] = global_img if global_img.mode == "RGBA" else global_img.convert("RGBA")
            state["local_img"] = local_img
            app.processed_image = local_img
            app.show_image(local_img)
            refresh_previews()

            analysis_text.config(state='normal')
            analysis_text.delete("1.0", tk.END)
            analysis_text.insert(
                "1.0",
                "Can bang toan cuc trai histogram rong nhung co the lam mat chi tiet vung. "
                f"Adaptive (tile {tile_var.get()} px) giup tang chi tiet o moi vung sang/toi."
            )
            analysis_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Loi", f"Khong can bang duoc:\n{e}")

    refresh_previews()
    app.show_image(app.original_image)


def create_convolution_ui(app, info_frame):
    title = tk.Label(info_frame, text="Demo Nhân chập (Convolution)",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    desc = tk.Label(info_frame, 
                   text="Demo nhân chập ma trận 5x5 với mask 3x3",
                   font=('Segoe UI', 9),
                   bg='white', fg='#7f8c8d')
    desc.pack(anchor='w', pady=(0, 15))

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w')

    result_frame = tk.Frame(info_frame, bg='white')
    result_frame.pack(fill='both', expand=True, pady=10)

    def run_demo():
        for widget in result_frame.winfo_children():
            widget.destroy()

        I, K = convolution.get_sample_matrices()
        I_conv = convolution.convolve_step(I, K)
        val, expl = convolution.manual_verification(I, K)

        def show_matrix(parent, matrix, title):
            frame = tk.Frame(parent, bg='white', padx=5)
            frame.pack(side='left', padx=5, anchor='n')
            tk.Label(frame, text=title, font=('Segoe UI', 9, 'bold'), bg='white').pack()
            
            text = ""
            for row in matrix:
                text += " ".join(f"{x:3}" for x in row) + "\n"
                
            lbl = tk.Label(frame, text=text, font=('Consolas', 10), bg='#ecf0f1', justify='left', padx=5, pady=5)
            lbl.pack(pady=5)

        matrices_frame = tk.Frame(result_frame, bg='white')
        matrices_frame.pack(fill='x', pady=10)

        show_matrix(matrices_frame, I, "Ma trận ảnh I (5x5)")
        show_matrix(matrices_frame, K, "Mask K (3x3)")
        show_matrix(matrices_frame, I_conv, "Kết quả I_conv")

        tk.Label(result_frame, text="Kiểm tra thủ công tại I(3,3) - (index 2,2):", 
                font=('Segoe UI', 9, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        tk.Label(result_frame, text=expl, font=('Consolas', 9), bg='#f9f9f9', fg='#27ae60', padx=10, pady=10, justify='left').pack(anchor='w', fill='x')


def create_my_convolution_ui(app, info_frame):
    """UI cho chức năng My Convolution Demo (New)"""
    title = tk.Label(info_frame, text="Demo Nhân chập (My Convolution)",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))

    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước để chạy demo.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    desc = tk.Label(info_frame, 
                   text="Áp dụng my_convolution (chạy 2 vòng lặp) với kernel làm nét (Sharpen) trên ảnh tải lên.\nLưu ý: Có thể mất vài giây với ảnh lớn.",
                   font=('Segoe UI', 9),
                   bg='white', fg='#7f8c8d', justify='left')
    desc.pack(anchor='w', pady=(0, 15))

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w')

    def run_on_image():
        # Convert to grayscale for simplicity
        gray = app.original_image.convert("L")
        img_arr = np.array(gray)
        
        # Sharpen kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        
        # Run convolution
        try:
             app.config(cursor="wait")
             app.update()
             
             result_arr = convolution.my_convolution(img_arr, kernel)
             
             # Clip result to 0-255
             result_arr = np.clip(result_arr, 0, 255).astype(np.uint8)
             result_img = Image.fromarray(result_arr)
             
             app.processed_image = result_img
             app.show_image(result_img)
             
             messagebox.showinfo("Hoàn tất", "Đã xử lý xong!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi xử lý: {e}")
        finally:
            app.config(cursor="")

    run_btn = tk.Button(btn_frame, text="Chạy nhân tích chập", 
                       command=run_on_image,
                       font=('Segoe UI', 9, 'bold'), bg='#9b59b6', fg='white',
                       relief='flat', cursor='hand2', padx=15, pady=8)
    run_btn.pack(side='left', padx=(0, 10))
    
    revert_btn = tk.Button(btn_frame, text="Quay về ảnh gốc",
                         command=lambda: app.show_image(app.original_image),
                         font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                         relief='flat', cursor='hand2', padx=15, pady=8)
    revert_btn.pack(side='left')


def create_edge_detection_ui(app, info_frame):
    """UI cho chức năng Dò biên (Edge Detection)"""
    title = tk.Label(info_frame, text="Dò biên (Edge Detection)",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    # Use clean imports inside function to avoid circular or early import issues
    from features import edge_detection
    import numpy as np
    
    nb = ttk.Notebook(info_frame)
    nb.pack(fill='both', expand=True, pady=10)
    
    # Tab 1: Sobel vs Prewitt
    f1 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f1, text="Sobel & Prewitt")
    
    desc1 = tk.Label(f1, text="So sánh Gradient bật 1: Sobel vs Prewitt", 
                    font=('Segoe UI', 9, 'italic'), bg='white', fg='#7f8c8d')
    desc1.pack(anchor='w', pady=(0, 10))
    
    # Slider
    thresh_frame1 = tk.Frame(f1, bg='white')
    thresh_frame1.pack(anchor='w', pady=(0, 10))
    tk.Label(thresh_frame1, text="Ngưỡng (Threshold):", bg='white').pack(side='left')
    thresh_var1 = tk.IntVar(value=40)
    tk.Scale(thresh_frame1, variable=thresh_var1, from_=0, to=255, orient='horizontal', bg='white', length=200).pack(side='left', padx=10)

    # Label phân tích cho Sobel/Prewitt (ẩn ban đầu)
    analysis_lbl1 = tk.Label(f1, text="", font=('Segoe UI', 9), 
                            bg='#ecf0f1', fg='#2c3e50', justify='left', wraplength=350, padx=10, pady=10)
    
    def run_sobel_prewitt():
        try:
             app.config(cursor="wait")
             app.update()
             
             gray = app.original_image.convert("L")
             img_arr = np.array(gray)
             th = thresh_var1.get()
             
             # Calculate
             sobel_res = edge_detection.apply_sobel(img_arr, threshold=th)
             prewitt_res = edge_detection.apply_prewitt(img_arr, threshold=th)
             
             # Convert to Images
             sobel_img = Image.fromarray(sobel_res)
             prewitt_img = Image.fromarray(prewitt_res)
             
             # Save one to processed for saving
             app.processed_image = sobel_img # Default save sobel
             
             # Display comparision
             imgs = [
                 ("Ảnh gốc", app.original_image.convert("L")),
                 ("Sobel", sobel_img),
                 ("Prewitt", prewitt_img)
             ]
             show_comparison(imgs)
             
             # Analysis text
             analysis = f"""PHÂN TÍCH (Ngưỡng={th}):
- Sobel: Kernel có trọng số 2 ở giữa giúp làm mịn và giảm nhiễu tốt hơn. Ảnh biên nhìn mượt hơn.
- Prewitt: Trọng số đều nhau, rất nhạy với nhiễu. Đường biên có thể sắc mảnh nhưng dễ bị đứt đoạn bởi nhiễu."""
             analysis_lbl1.config(text=analysis)
             analysis_lbl1.pack(anchor='w', fill='x', pady=10)
             
        except Exception as e:
            messagebox.showerror("Lỗi", f"{e}")
        finally:
             app.config(cursor="")
             
    btn1 = tk.Button(f1, text="Chạy so sánh", command=run_sobel_prewitt,
                    font=('Segoe UI', 9, 'bold'), bg='#2980b9', fg='white',
                    relief='flat', padx=15, pady=5)
    btn1.pack(anchor='w')


    # Tab 2: Robert vs Kirsch
    f2 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f2, text="Robert & Kirsch")
    
    desc2 = tk.Label(f2, text="So sánh: Robert (2x2) vs Kirsch (8 hướng)", 
                    font=('Segoe UI', 9, 'italic'), bg='white', fg='#7f8c8d')
    desc2.pack(anchor='w', pady=(0, 10))

    # Slider
    thresh_frame2 = tk.Frame(f2, bg='white')
    thresh_frame2.pack(anchor='w', pady=(0, 10))
    tk.Label(thresh_frame2, text="Ngưỡng (Threshold):", bg='white').pack(side='left')
    thresh_var2 = tk.IntVar(value=40)
    tk.Scale(thresh_frame2, variable=thresh_var2, from_=0, to=255, orient='horizontal', bg='white', length=200).pack(side='left', padx=10)
    
    # Label phân tích cho Robert/Kirsch
    analysis_lbl2 = tk.Label(f2, text="", font=('Segoe UI', 9), 
                            bg='#ecf0f1', fg='#2c3e50', justify='left', wraplength=350, padx=10, pady=10)

    def run_robert_kirsch():
        try:
             app.config(cursor="wait")
             app.update()
             
             gray = app.original_image.convert("L")
             img_arr = np.array(gray)
             th = thresh_var2.get()
             
             # Calculate
             robert_res = edge_detection.apply_roberts(img_arr, threshold=th)
             kirsch_res = edge_detection.apply_kirsch(img_arr, threshold=th)
             
             # Convert to Images
             robert_img = Image.fromarray(robert_res)
             kirsch_img = Image.fromarray(kirsch_res)
             
             app.processed_image = kirsch_img
             
             # Display comparision
             imgs = [
                 ("Ảnh gốc", app.original_image.convert("L")),
                 ("Robert (2x2)", robert_img),
                 ("Kirsch (8 hướng)", kirsch_img)
             ]
             show_comparison(imgs)
             
             # Analysis text
             analysis = f"""PHÂN TÍCH (Ngưỡng={th}):
- Robert: Kernel 2x2 nhỏ, tính nhanh nhưng RẤT nhạy nhiễu muối tiêu.
- Kirsch: Dò 8 hướng lấy max. Biên cực kỳ rõ và ít nhiễu hơn Robert. Tốt nhất trong các phương pháp trên."""
             analysis_lbl2.config(text=analysis)
             analysis_lbl2.pack(anchor='w', fill='x', pady=10)
             
        except Exception as e:
            messagebox.showerror("Lỗi", f"{e}")
        finally:
             app.config(cursor="")

    btn2 = tk.Button(f2, text="Chạy so sánh", command=run_robert_kirsch,
                    font=('Segoe UI', 9, 'bold'), bg='#8e44ad', fg='white',
                    relief='flat', padx=15, pady=5)
    btn2.pack(anchor='w')

    def show_comparison(image_list):
        # Helper to show images horizontally
        try:
             app.text_frame.pack_forget()
        except: pass
        app.canvas.master.pack(fill='both', expand=True)
        app.canvas.delete("all")
        
        W = app.canvas.winfo_width() or 800
        H = app.canvas.winfo_height() or 600
        
        n_imgs = len(image_list)
        spacing = 10
        img_w = (W - (n_imgs+1) * spacing) // n_imgs
        img_h = H - 50 
        
        current_x = spacing
        
        app.comparison_photos = [] 
        
        for title, pil_img in image_list:
            w, h = pil_img.size
            ratio = min(img_w/w, img_h/h)
            new_size = (int(w*ratio), int(h*ratio))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            
            p = ImageTk.PhotoImage(resized)
            app.comparison_photos.append(p)
            
            y_pos = H // 2
            x_pos = current_x + img_w // 2
            
            app.canvas.create_image(x_pos, y_pos, image=p, anchor="center")
            app.canvas.create_text(x_pos, y_pos + new_size[1]//2 + 15, text=title, font=('Segoe UI', 10, 'bold'), fill='#2c3e50')
            
            current_x += img_w + spacing


def create_average_filter_ui(app, info_frame):
    title = tk.Label(info_frame, text="Lọc trung bình (Blur/Denoise)",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    state = {'noisy': None, 'filtered_3': None, 'filtered_5': None}

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w', pady=(0, 15))

    def show_comparison():
        for widget in display_frame.winfo_children():
            widget.destroy()

        imgs = [
            ("Ảnh gốc", app.original_image),
            ("Ảnh nhiễu (Muối tiêu)", state['noisy']),
            (f"Lọc trung bình {state.get('last_filter', '')}", app.processed_image)
        ]

        for name, img in imgs:
            if img:
                wrapper = tk.Frame(display_frame, bg='white')
                wrapper.pack(side='left', padx=5, expand=True)
                
                tk.Label(wrapper, text=name, font=('Segoe UI', 9, 'bold'), bg='white').pack()
                
                c = tk.Canvas(wrapper, width=200, height=200, bg='#ecf0f1', highlightthickness=1)
                c.pack()
                
                # Resize trực tiếp vì canvas chưa có kích thước thật
                disp = img.copy()
                disp.thumbnail((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(disp)
                c.create_image(100, 100, image=photo, anchor='center')
                c.image = photo

    def add_noise():
        state['noisy'] = noise.add_salt_and_pepper_noise(app.original_image)
        app.processed_image = state['noisy']
        state['last_filter'] = '(Chưa lọc)'
        show_comparison()
        
    def filter_3x3():
        if state['noisy'] is None:
            messagebox.showwarning("Chưa có nhiễu", "Vui lòng thêm nhiễu trước.")
            return
        res = noise.apply_average_filter(state['noisy'], 3)
        app.processed_image = res
        state['last_filter'] = '3x3'
        show_comparison()
        update_analysis(3)

    def filter_5x5():
        if state['noisy'] is None:
            messagebox.showwarning("Chưa có nhiễu", "Vui lòng thêm nhiễu trước.")
            return
        res = noise.apply_average_filter(state['noisy'], 5)
        app.processed_image = res
        state['last_filter'] = '5x5'
        show_comparison()
        update_analysis(5)

    def update_analysis(size):
        text_widget.config(state='normal')
        text_widget.delete('1.0', tk.END)
        if size == 3:
            msg = "Bộ lọc 3x3: Khử được một phần nhiễu muối tiêu nhưng vẫn còn sót lại. Ảnh bị mờ đi một chút so với ảnh gốc."
        else:
            msg = "Bộ lọc 5x5: Khử nhiễu tốt hơn 3x3 (ảnh `mịn` hơn) nhưng làm ảnh bị mờ (blur) rõ rệt hơn. Các chi tiết cạnh bị nhòe đi nhiều."
        text_widget.insert('1.0', msg)
        text_widget.config(state='disabled')

    tk.Button(btn_frame, text="1. Thêm nhiễu", command=add_noise,
             font=('Segoe UI', 9), bg='#e74c3c', fg='white', relief='flat', padx=10).pack(side='left', padx=2)
             
    tk.Button(btn_frame, text="2. Lọc 3x3", command=filter_3x3,
             font=('Segoe UI', 9), bg='#3498db', fg='white', relief='flat', padx=10).pack(side='left', padx=2)
             
    tk.Button(btn_frame, text="3. Lọc 5x5", command=filter_5x5,
             font=('Segoe UI', 9), bg='#2980b9', fg='white', relief='flat', padx=10).pack(side='left', padx=2)

    display_frame = tk.Frame(info_frame, bg='white')
    display_frame.pack(fill='x', pady=10)

    tk.Label(info_frame, text="Phân tích hiệu quả:", font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w')
    
    text_widget = tk.Text(info_frame, height=4, font=('Segoe UI', 9), bg='#f8f9fa', relief='flat', padx=5, pady=5)
    text_widget.pack(fill='x', pady=5)
    text_widget.insert('1.0', "Hãy thêm nhiễu và thử lọc để xem kết quả.")
    text_widget.config(state='disabled')


def create_median_filter_ui(app, info_frame):
    title = tk.Label(info_frame, text="Lọc trung vị (Median)",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    state = {'noisy': None}

    btn_frame = tk.Frame(info_frame, bg='white')
    btn_frame.pack(anchor='w', pady=(0, 15))

    def show_comparison(avg_img, median_img, size):
        for widget in display_frame.winfo_children():
            widget.destroy()

        imgs = [
            (f"Ảnh nhiễu", state['noisy']),
            (f"Trung bình {size}x{size}", avg_img),
            (f"Trung vị {size}x{size}", median_img)
        ]

        for name, img in imgs:
            if img:
                wrapper = tk.Frame(display_frame, bg='white')
                wrapper.pack(side='left', padx=5, expand=True)
                
                tk.Label(wrapper, text=name, font=('Segoe UI', 9, 'bold'), bg='white').pack()
                
                c = tk.Canvas(wrapper, width=200, height=200, bg='#ecf0f1', highlightthickness=1)
                c.pack()
                
                # Use fixed size to avoid display issues
                disp = img.copy()
                disp.thumbnail((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(disp)
                c.create_image(100, 100, image=photo, anchor='center')
                c.image = photo

    def add_noise():
        state['noisy'] = noise.add_salt_and_pepper_noise(app.original_image)
        app.processed_image = state['noisy']
        
        # Clear display
        for widget in display_frame.winfo_children():
            widget.destroy()
            
        # Show noisy image only
        wrapper = tk.Frame(display_frame, bg='white')
        wrapper.pack(side='left', padx=5, expand=True)
        tk.Label(wrapper, text="Ảnh nhiễu", font=('Segoe UI', 9, 'bold'), bg='white').pack()
        c = tk.Canvas(wrapper, width=200, height=200, bg='#ecf0f1', highlightthickness=1)
        c.pack()
        disp = state['noisy'].copy()
        disp.thumbnail((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(disp)
        c.create_image(100, 100, image=photo, anchor='center')
        c.image = photo
        
        update_analysis(0)

    def run_compare(size):
        if state['noisy'] is None:
            messagebox.showwarning("Chưa có nhiễu", "Vui lòng thêm nhiễu trước.")
            return
            
        # Run both filters
        avg_res = noise.apply_average_filter(state['noisy'], size)
        median_res = noise.apply_median_filter(state['noisy'], size)
        
        # Save median as processed for main display if needed, but here we show comparison
        app.processed_image = median_res
        
        show_comparison(avg_res, median_res, size)
        update_analysis(size)

    def update_analysis(size):
        text_widget.config(state='normal')
        text_widget.delete('1.0', tk.END)
        if size == 0:
             msg = "Hãy thêm nhiễu trước."
        elif size == 3:
            msg = "So sánh 3x3:\n- Trung bình: Làm mờ ảnh, nhiễu vẫn còn (dạng đốm mờ).\n- Trung vị: Khử sạch nhiễu muối tiêu, giữ lại cạnh sắc nét hơn hẳn. Trung vị tốt hơn vì nó loại bỏ giá trị cực đoan (0/255) thay vì chia đều chúng."
        else:
            msg = "So sánh 5x5:\n- Trung bình: Ảnh rất mờ, mất chi tiết.\n- Trung vị: Vẫn khử nhiễu tốt và giữ cạnh, nhưng các chi tiết nhỏ có thể bị mất hoặc biến dạng (bệt màu) nếu kích thước mask quá lớn."
        text_widget.insert('1.0', msg)
        text_widget.config(state='disabled')

    tk.Button(btn_frame, text="1. Thêm nhiễu", command=add_noise,
             font=('Segoe UI', 9), bg='#e74c3c', fg='white', relief='flat', padx=10).pack(side='left', padx=2)
             
    tk.Button(btn_frame, text="So sánh 3x3", command=lambda: run_compare(3),
             font=('Segoe UI', 9), bg='#3498db', fg='white', relief='flat', padx=10).pack(side='left', padx=2)
             
    tk.Button(btn_frame, text="So sánh 5x5", command=lambda: run_compare(5),
             font=('Segoe UI', 9), bg='#2980b9', fg='white', relief='flat', padx=10).pack(side='left', padx=2)

    display_frame = tk.Frame(info_frame, bg='white')
    display_frame.pack(fill='x', pady=10)

    tk.Label(info_frame, text="Phân tích hiệu quả:", font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w')
    
    text_widget = tk.Text(info_frame, height=6, font=('Segoe UI', 9), bg='#f8f9fa', relief='flat', padx=5, pady=5)
    text_widget.pack(fill='x', pady=5)
    text_widget.insert('1.0', "Hãy thêm nhiễu và thử lọc để so sánh.")
    text_widget.config(state='disabled')


def create_laplace_features_ui(app, info_frame):
    title = tk.Label(info_frame, text="Laplace & LoG & Sharpening",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white', fg='#2c3e50')
    title.pack(anchor='w', pady=(0, 10))
    
    if app.original_image is None:
        tk.Label(info_frame, text="Vui lòng tải ảnh lên trước.",
                font=('Segoe UI', 9), bg='white', fg='#e74c3c').pack(anchor='w')
        return

    from features import laplace_processing, noise
    import numpy as np
    import math
    
    nb = ttk.Notebook(info_frame)
    nb.pack(fill='both', expand=True, pady=10)
    
    # helper for showing images on main canvas
    def show_on_canvas(image_list):
        try:
             app.text_frame.pack_forget()
        except: pass
        app.canvas.master.pack(fill='both', expand=True)
        app.canvas.delete("all")
        
        W = app.canvas.winfo_width() or 800
        H = app.canvas.winfo_height() or 600
        
        n_imgs = len(image_list)
        # Dynamic spacing
        spacing = 20
        # Check if we have 2 rows (more than 3 images?)
        rows = 1
        if n_imgs > 3:
            rows = 2
            
        img_w = (W - (math.ceil(n_imgs/rows)+1) * spacing) // math.ceil(n_imgs/rows)
        img_h = (H - 50) // rows
        
        app.comparison_photos = [] 
        
        cols = math.ceil(n_imgs / rows)
        
        for idx, (title, pil_img) in enumerate(image_list):
            row = idx // cols
            col = idx % cols
            
            # Resize
            w, h = pil_img.size
            ratio = min(img_w/w, img_h/h)
            new_size = (int(w*ratio), int(h*ratio))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            
            p = ImageTk.PhotoImage(resized)
            app.comparison_photos.append(p)
            
            # Position
            x_pos = spacing + col * (img_w + spacing) + img_w // 2
            y_pos = row * (img_h + 30) + img_h // 2 + 30 # offset top
            
            app.canvas.create_image(x_pos, y_pos, image=p, anchor="center")
            app.canvas.create_text(x_pos, y_pos + new_size[1]//2 + 15, text=title, font=('Segoe UI', 10, 'bold'), fill='#2c3e50')

    f1 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f1, text="Laplace")
    
    tk.Label(f1, text="Dò biên Laplace (Đạo hàm bậc 2)", bg='white').pack(anchor='w')
    
    state_91 = {'noisy': None}
    
    def add_noise_91():
        state_91['noisy'] = noise.add_salt_and_pepper_noise(app.original_image)
        tk.messagebox.showinfo("Info", "Đã thêm nhiễu muối tiêu")
        
    def run_91():
        try:
            app.config(cursor="wait")
            app.update()
            
            # Use noisy image if available, else original
            if state_91['noisy']:
                src_img = state_91['noisy']
                src_label = "Ảnh nhiễu"
            else:
                src_img = app.original_image
                src_label = "Ảnh gốc"
            
            gray = src_img.convert("L")
            img_arr = np.array(gray)
            
            # Run 4N and 8N
            res4n = laplace_processing.apply_laplace(img_arr, '4n_neg')
            res8n = laplace_processing.apply_laplace(img_arr, '8n_neg')
            
            img4n = Image.fromarray(res4n)
            img8n = Image.fromarray(res8n)
            
            app.processed_image = img8n
            
            imgs = [
                (src_label, gray),
                ("Laplace 4-neighbors", img4n),
                ("Laplace 8-neighbors", img8n)
            ]
            show_on_canvas(imgs)
            
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
        finally:
            app.config(cursor="")
            
    tk.Button(f1, text="1. Thêm nhiễu (Tùy chọn)", command=add_noise_91, bg='#e74c3c', fg='white', relief='flat').pack(pady=5, anchor='w')
    tk.Button(f1, text="2. Chạy Laplace", command=run_91, bg='#3498db', fg='white', relief='flat').pack(pady=5, anchor='w')
    
    f2 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f2, text="LoG")
    tk.Label(f2, text="Laplacian of Gaussian (Khử nhiễu -> Laplace)", bg='white', wraplength=200, justify='left').pack(anchor='w')
    
    state_92 = {'noisy': None}
    
    def add_noise_92():
        state_92['noisy'] = noise.add_salt_and_pepper_noise(app.original_image)
        tk.messagebox.showinfo("Info", "Đã xong thêm nhiễu muối tiêu")
        
    def run_92():
        if state_92['noisy'] is None:
            messagebox.showwarning("Warning", "Hãy thêm nhiễu trước")
            return
            
        try:
            app.config(cursor="wait")
            app.update()
            
            gray = state_92['noisy'].convert("L")
            img_arr = np.array(gray)
            
            # 1. Pure Laplace on Noisy
            raw_res = laplace_processing.apply_laplace(img_arr, '4n_neg')
            
            # 2. LoG
            log_res = laplace_processing.apply_log(img_arr, '4n_neg')
            
            img_raw = Image.fromarray(raw_res)
            img_log = Image.fromarray(log_res)
            
            app.processed_image = img_log
            
            imgs = [
                ("Ảnh nhiễu", gray),
                ("Laplace (Ồn)", img_raw),
                ("LoG (Mượt hơn)", img_log)
            ]
            show_on_canvas(imgs)
            
            analysis = "PHÂN TÍCH:\n- Laplace thuần: Cực kỳ nhạy cảm với nhiễu, các hạt nhiễu biến thành biên giả.\n- LoG: Gaussian làm mịn nhiễu trước, nên Laplace chỉ bắt được các biên thực tế. Ảnh sạch hơn nhiều."
            analysis_lbl2.config(text=analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
        finally:
             app.config(cursor="")

    tk.Button(f2, text="Thêm nhiễu", command=add_noise_92, bg='#e74c3c', fg='white', relief='flat').pack(pady=5, anchor='w')
    tk.Button(f2, text="Chạy & So sánh", command=run_92, bg='#9b59b6', fg='white', relief='flat').pack(pady=5, anchor='w')
    
    analysis_lbl2 = tk.Label(f2, text="", bg='#ecf0f1', fg='#2c3e50', justify='left', wraplength=350, padx=5, pady=5)
    analysis_lbl2.pack(fill='x', pady=10)

    # --- 9.3 Smooth Sobel vs LoG ---
    f3 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f3, text="9.3 SoG vs LoG")
    tk.Label(f3, text="Làm mịn + Sobel vs LoG", bg='white').pack(anchor='w')
    
    state_93 = {'noisy': None}
    def add_noise_93():
        state_93['noisy'] = noise.add_salt_and_pepper_noise(app.original_image)
        tk.messagebox.showinfo("Info", "Đã xong thêm nhiễu muối tiêu")

    def run_93():
        if state_93['noisy'] is None:
            messagebox.showwarning("Warning", "Hãy thêm nhiễu trước")
            return
            
        try:
            app.config(cursor="wait")
            app.update()
            
            gray = state_93['noisy'].convert("L")
            img_arr = np.array(gray)
            
            # 1. Smooth + Sobel
            sog_res = laplace_processing.apply_smooth_sobel(img_arr)
            
            # 2. LoG
            log_res = laplace_processing.apply_log(img_arr, '4n_neg')
            
            img_sog = Image.fromarray(sog_res)
            img_log = Image.fromarray(log_res)
            
            app.processed_image = img_log
            
            imgs = [
                ("Ảnh nhiễu", gray),
                ("Smooth + Sobel", img_sog),
                ("LoG", img_log)
            ]
            show_on_canvas(imgs)
            
            analysis = "PHÂN TÍCH:\n- Smooth+Sobel: Biên thường dày hơn (do Sobel + Gaussian lan tỏa).\n- LoG: Biên mảnh hơn (zero-crossing), xác định vị trí biên chính xác hơn nhưng đôi khi mất chi tiết nhỏ."
            analysis_lbl3.config(text=analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
        finally:
             app.config(cursor="")

    tk.Button(f3, text="Thêm nhiễu", command=add_noise_93, bg='#e74c3c', fg='white', relief='flat').pack(pady=5, anchor='w')
    tk.Button(f3, text="Chạy & So sánh", command=run_93, bg='#27ae60', fg='white', relief='flat').pack(pady=5, anchor='w')
    
    analysis_lbl3 = tk.Label(f3, text="", bg='#ecf0f1', fg='#2c3e50', justify='left', wraplength=350, padx=5, pady=5)
    analysis_lbl3.pack(fill='x', pady=10)

    f4 = tk.Frame(nb, bg='white', padx=10, pady=10)
    nb.add(f4, text="Sharpen")
    tk.Label(f4, text="Làm nét ảnh bằng Laplace", bg='white').pack(anchor='w')
    
    def run_94():
        try:
            app.config(cursor="wait")
            app.update()
            
            gray = app.original_image.convert("L")
            img_arr = np.array(gray)
            
            # Sharpen using 4 kernels
            # 1. 4N Neg (Center -4) -> Subtract
            s1 = laplace_processing.apply_sharpening(img_arr, '4n_neg')
            # 2. 8N Neg (Center -8) -> Subtract
            s2 = laplace_processing.apply_sharpening(img_arr, '8n_neg')
            # 3. 4N Pos (Center 4) -> Add
            s3 = laplace_processing.apply_sharpening(img_arr, '4n_pos')
            # 4. 8N Pos (Center 8) -> Add
            s4 = laplace_processing.apply_sharpening(img_arr, '8n_pos')
            
            imgs = [
                ("Gốc", gray),
                ("4N (-4)", Image.fromarray(s1)),
                ("8N (-8)", Image.fromarray(s2)),
                ("4N (+4)", Image.fromarray(s3)),
                ("8N (+8)", Image.fromarray(s4))
            ]
            
            app.processed_image = Image.fromarray(s2)
            show_on_canvas(imgs)
            
            analysis = "PHÂN TÍCH:\n- Cả 4 kernel đều làm nét ảnh.\n- Kết quả phép TRỪ với kernel tâm ÂM tương đương phép CỘNG với kernel tâm DƯƠNG.\n- Kernel 8-hàng xóm thường cho kết quả sắc nét hơn (mạnh hơn)."
            analysis_lbl4.config(text=analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
        finally:
             app.config(cursor="")
             
    tk.Button(f4, text="Chạy làm nét", command=run_94, bg='#f39c12', fg='white', relief='flat').pack(pady=5, anchor='w')
    analysis_lbl4 = tk.Label(f4, text="", bg='#ecf0f1', fg='#2c3e50', justify='left', wraplength=350, padx=5, pady=5)
    analysis_lbl4.pack(fill='x', pady=10)
