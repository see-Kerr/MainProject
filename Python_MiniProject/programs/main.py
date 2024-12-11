import tkinter as tk
from tkinter import filedialog
import numpy as np
import coordsData
import getPixel
import threading
import queue
import speech_recognition as sr
from tkinter import ttk
import portion
import pyttsx3
 
# init function to get an engine instance for the speech synthesis 
engine = pyttsx3.init()
 
# say method on the engine that passing input text to be spo

end, pv = [0, 0], [0, 0]
Y = 15
speech_queue = queue.Queue()
current_text = ""


def speech_recognition_thread(speech_queue):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            speech_queue.put(text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass


def Main(image_path, root):
    global current_text

    root.title("Notebook")
    root.geometry("850x700")

    title_bar = tk.Frame(root, bg="#FF6F61", relief='flat', bd=0)
    title_bar.pack(fill=tk.X)

    title_label = ttk.Label(title_bar, text="HANDWRITING DIGITIZATION", background="#FF6F61", foreground="white", font=("Helvetica Neue", 20))
    title_label.pack(pady=10)

    coordinates = coordsData.getData(image_path)
    pixels = {chr(97 + i): coordinates[i] for i in range(26)}
    refmin, refmax = min(coord[1] for coord in pixels["a"]), max(coord[1] for coord in pixels["a"])
    ref = (refmin, refmax)

    portion.getData(image_path)

    for key in pixels:
        pixels[key] = getPixel.align(pixels[key], ref, key)

    # Clear any existing content and set up the canvas
    for widget in root.winfo_children():
        widget.destroy()

    def draw_coordinates(canvas, coordinates, sx=1, sy=1, end=[0, 0], col='#000000'):
        global Y
        coordinate = coordinates * np.array([sx, sy])
        coordinate = coordinate.tolist()
        for (x, y) in coordinate:
            canvas.create_line(x + end[0] + 20, y + 40 + Y, x + end[0] + 21.5, y + 41 + Y, fill=col, width=0.1, splinesteps=100)
        return coordinate[-1]

    def new_page(canvas):
        global current_text, Y, end
        canvas.delete("all")
        current_text = ""
        Y = 15
        end = [0, 0]

    def save_page():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(current_text)

    def on_key_press(event):
        global end, pv, Y, current_text
        #print(event)
        if end[1] < -1000:
            Y += 60
            end = [0, 0]
        key = event.char.lower()
        if key == " ":
            end = [end[0] + 20, end[1]]
            current_text += " "
        elif key == "\r":
            Y += 45
            end = [0, 0]
            current_text += "\n"
        elif key=="\x08":
            print("backspace")
            
        elif key:
            if key in pixels:
                pv = draw_coordinates(canvas, pixels[key], 1, 1, end)
                end = np.add(pv, end)
                current_text += key

    def handle_typing(event):
        global current_text
        #print(event.keysm)
        if event.keysym == "Return":
            for char in current_text:
                root.event_generate('<KeyPress>', keysym=char)
            root.event_generate('<KeyPress>', keysym='Return')
            current_text = ""
            entry.delete(0, tk.END)
        elif event == "\x08":
            #print(event.keysm)
            #print("!!!")
            if current_text:
                current_text = current_text[:-1]
                entry.delete(0, tk.END)
                entry.insert(0, current_text)
        else:
            current_text += event.char
            entry.delete(0, tk.END)
            entry.insert(0, current_text)

    def process_speech_input():
        global current_text
        while not speech_queue.empty():
            try:
                spoken_text = speech_queue.get_nowait()
                print(spoken_text)
                engine.say(spoken_text)
                engine.runAndWait()
                for char in spoken_text + " ":
                    root.event_generate('<KeyPress>', keysym=char)
            except queue.Empty:
                pass
        root.after(100, process_speech_input)

    canvas = tk.Canvas(root, bg='white', width=1100, height=830)
    canvas.pack(fill=tk.BOTH, expand=True)

    root.bind('<KeyPress>', on_key_press)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)
    entry.bind('<KeyPress>', handle_typing)

    menu = tk.Menu(root)
    root.config(menu=menu)
    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_page(canvas))
    file_menu.add_command(label="Save", command=save_page)

    threading.Thread(target=speech_recognition_thread, args=(speech_queue,), daemon=True).start()
    process_speech_input()
