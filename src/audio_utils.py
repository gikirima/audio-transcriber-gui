import ffmpeg
import os

def convert_to_wav(input_path, output_path=None):
    # Jika sudah WAV, langsung return path-nya
    if input_path.lower().endswith(".wav"):
        return input_path
    
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".wav"
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"File berhasil dikonversi ke: {output_path}")
        return output_path
    except ffmpeg.Error as e:
        print("Gagal konversi:", e)
        return None