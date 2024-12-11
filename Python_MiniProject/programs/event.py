import tkinter as tk

def on_key_press(event):
    print(f"Key pressed: {event.keysym}")

def on_key_release(event):
    print(f"Key released: {event.keysym}")

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Keyboard Events in Tkinter")

    # Create a label to display instructions
    label = tk.Label(root, text="Press any key to see the events.")
    label.pack(pady=20)

    # Bind key press and key release events
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
