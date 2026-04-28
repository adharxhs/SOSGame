import gui
import tkinter as tk

def main():
    root = tk.Tk()
    gui.set_icon(root)
    app = gui.SOSGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
