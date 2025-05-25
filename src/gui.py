from tkinter import Tk, Frame, Label, Button, StringVar, OptionMenu, filedialog, Text, messagebox
from tkinter import ttk
import os
import audio_utils
from transcriber import Transcriber
import threading

WHISPER_MODELS = [
    "base",
    "small",
    "turbo"
]

class AudioTranscriberGUI:
    def __init__(self, master):
        self.master = master
        master.title("Audio Transcriber")

        self.frame = Frame(master)
        self.frame.pack(padx=10, pady=10)

        self.label = Label(self.frame, text="Browse your audio file:")
        self.label.pack()

        # Frame horizontal untuk text_area dan browse_button
        self.input_frame = Frame(self.frame)
        self.input_frame.pack(pady=5)

        self.text_area = Text(self.input_frame, height=1, width=50)
        self.text_area.pack(side="left", padx=(0, 5))

        self.browse_button = Button(self.input_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side="left")

        # Frame horizontal untuk dropdown model dan language
        self.select_frame = Frame(self.frame)
        self.select_frame.pack(pady=5)

        self.model_label = Label(self.select_frame, text="Pilih model Whisper:")
        self.model_label.pack(side="left", padx=(0, 5))

        self.model_var = StringVar(master)
        self.model_var.set("base")  # default value
        self.model_menu = OptionMenu(self.select_frame, self.model_var, *WHISPER_MODELS)
        self.model_menu.pack(side="left", padx=(0, 15))

        self.language_label = Label(self.select_frame, text="Pilih bahasa:")
        self.language_label.pack(side="left", padx=(0, 5))

        self.language_var = StringVar(master)
        self.language_var.set("Pilih Bahasa")  # default value
        self.language_menu = OptionMenu(self.select_frame, self.language_var, *self.get_supported_languages())
        self.language_menu.pack(side="left")

        # Warning di bawah progress bar
        self.warning_label = Label(self.frame, text="Warning! tidak bisa dihentikan setelah mulai transkripsi.", fg="red")
        self.warning_label.pack(pady=(5, 0))

        # Progress bar dan status label (langsung di bawah select_frame)
        self.progress = ttk.Progressbar(self.frame, mode="indeterminate")        
        self.status_label = Label(self.frame, text="---", fg="blue")

        # Tombol untuk transkripsi di bawah warning
        self.transcribe_button = Button(self.frame, text="Transcribe", command=self.start_transcribe_thread)
        self.transcribe_button.pack(pady=0)

    def get_supported_languages(self):
        from languages import supported_languages
        return supported_languages

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.m4a")])
        if file_path:
            self.text_area.delete(1.0, "end")
            self.text_area.insert("end", file_path)

    def start_transcribe_thread(self):
        self.transcribe_button.config(state="disabled")
        self.progress.pack(pady=(5, 0), before=self.transcribe_button)
        self.status_label.pack(pady=(0, 5), before=self.transcribe_button)
        self.progress.start(10)
        self.set_status("Mengonversi audio...")
        threading.Thread(target=self.transcribe_audio).start()

    def set_status(self, text):
        self.status_label.config(text=text)
        self.status_label.update_idletasks()

    def reset_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.pack_forget()

        self.progress.pack(pady=(5, 0), before=self.transcribe_button)
        self.status_label.pack(pady=(0, 5), before=self.transcribe_button)
        self.status_label.config(text="---")
        self.transcribe_button.config(state="normal")

    def transcribe_audio(self):
        audio_file = self.text_area.get(1.0, "end-1c").strip()
        language = self.language_var.get()
        model_name = self.model_var.get()

        if not audio_file or not os.path.isfile(audio_file):
            self.set_status("")
            messagebox.showerror("Error", "Pilih file audio yang valid!")
            self.reset_progress()
            return

        if language == "Pilih Bahasa":
            self.set_status("")
            messagebox.showerror("Error", "Pilih bahasa!")
            self.reset_progress()
            return

        # Konversi audio
        self.set_status("Mengonversi audio ke WAV...")
        wav_file = audio_utils.convert_to_wav(audio_file)
        if not wav_file or not os.path.isfile(wav_file):
            self.set_status("")
            messagebox.showerror("Error", "Gagal konversi audio ke WAV. Pastikan file audio valid dan ffmpeg terinstall.")
            self.reset_progress()
            return
        
        model_path = os.path.join("models", f"{model_name}.pt")
        if not os.path.exists(model_path):
            self.set_status("Model belum ada, akan diunduh otomatis oleh Whisper...")
        else:
            self.set_status(f"Model {model_name} sudah tersedia, melanjutkan transkripsi...")
        self.set_status("Model siap, mulai transkripsi...")
        self.status_label.update_idletasks()

        # Transkripsi
        self.set_status("Mentranskripsi audio...")
        transcriber = Transcriber(model_name=model_name)
        try:
            result = transcriber.transcribe(wav_file, language=language)
        except Exception as e:
            self.set_status("")
            messagebox.showerror("Error", f"Transcription failed: {e}")
            self.reset_progress()
            return

        # Simpan hasil
        self.set_status("Menyimpan hasil transkripsi...")
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(result)
            messagebox.showinfo("Success", "Transcription saved successfully!")
        self.set_status("Selesai.")
        self.reset_progress()

    def reset_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.transcribe_button.config(state="normal")

def main():
    root = Tk()
    app = AudioTranscriberGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()