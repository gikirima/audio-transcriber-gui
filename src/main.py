import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gui import AudioTranscriberGUI

def main():
    # Initialize the main application window
    root = tk.Tk()
    root.title("Audio Transcriber")
    
    # Create and run the GUI
    app = AudioTranscriberGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()