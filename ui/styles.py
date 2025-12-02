from tkinter import ttk


def setup_styles():
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
