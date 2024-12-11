import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import main  
import textToHandwriting


def navigate_to_upload_image(token):
    # Clear the current widgets in the frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Add the "Upload Image" button
    upload_button = ttk.Button(frame, text="Upload Image", command=lambda: upload_image(token))
    upload_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def convert_image_to_text():
    print("Convert Image to Text selected.")
    navigate_to_upload_image(0)


def type_into_handwriting():    
    print("Type into Handwriting selected.")
    navigate_to_upload_image(1)


def upload_image(token):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        progress = ttk.Progressbar(frame, orient="horizontal", mode="indeterminate")
        progress.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        progress.start()
        
        try:
            if (token == 0):
                textToHandwriting.Main(file_path, root)
            else:
                main.Main(file_path, root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the image: {e}")

def draw_striped_pattern(canvas, width, height, stripe_width=20):
    colors = ["#f9f9f9", "#ffffff"]
    for i in range(0, height, stripe_width):
        color = colors[(i // stripe_width) % 2]
        canvas.create_rectangle(0, i, width, i + stripe_width, fill=color, outline=color)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def create_main_app():
    global root, frame
    root = tk.Tk()
    root.title("Handwriting Digitization")
    root.geometry("850x700")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica Neue", 14), padding=10, borderwidth=0)
    style.map("TButton", background=[("active", "#FF6F61")], foreground=[("active", "white")])
    style.configure("TLabel", font=("Helvetica Neue", 16), padding=5, background="#FFFFFF", foreground="#333333")

    title_bar = tk.Frame(root, bg="#FF6F61", relief='flat', bd=0)
    title_bar.pack(fill=tk.X)

    title_label = ttk.Label(title_bar, text="HANDWRITING DIGITIZATION", background="#FF6F61", foreground="white", font=("Helvetica Neue", 20))
    title_label.pack(pady=10)

    frame = ttk.Frame(root, padding=(20, 10, 20, 10), relief='flat')
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame, width=800, height=600, bg="white", highlightthickness=0)
    canvas.pack(expand=True)
    draw_striped_pattern(canvas, 800, 600)

    # Buttons for initial functionalities
    button1 = ttk.Button(frame, text="Convert Image to Text", command=convert_image_to_text)
    button1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button2 = ttk.Button(frame, text="Type into Handwriting", command=type_into_handwriting)
    button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    footer_label = ttk.Label(frame, text="Select an option to get started", background="white", font=("Helvetica Neue", 14))
    footer_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


# Run the main app
create_main_app()
