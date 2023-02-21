import os
import threading
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import AudioFileClip

class Converter:
    def __init__(self, input_dir, output_dir, max_threads):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.max_threads = max_threads

    def _convert_file(self, filename):
        input_path = os.path.join(self.input_dir, filename)
        output_path = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}.mp3")
        with AudioFileClip(input_path) as audio:
            audio.write_audiofile(output_path, verbose=False)

    def convert_files(self):
        print(f"Converting files in {self.input_dir} to {self.output_dir}...")
        filenames = os.listdir(self.input_dir)
        threads = []
        for filename in filenames:
            if filename.endswith(".mp4"):
                while threading.active_count() >= self.max_threads:
                    continue
                thread = threading.Thread(target=self._convert_file, args=(filename,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
        print("Conversion complete!")


class UX:
    def __init__(self):
        self.input_dir = ""
        self.output_dir = ""
        self.max_threads = 4

        self.root = tk.Tk()
        self.root.title("MP4 to MP3 Converter")
        self.root.geometry("400x200")

        input_label = tk.Label(self.root, text="Input Directory:")
        input_label.pack()

        self.input_entry = tk.Entry(self.root)
        self.input_entry.pack()

        input_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        input_button.pack()

        output_label = tk.Label(self.root, text="Output Directory:")
        output_label.pack()

        self.output_entry = tk.Entry(self.root)
        self.output_entry.pack()

        output_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        output_button.pack()

        threads_label = tk.Label(self.root, text="Max Threads:")
        threads_label.pack()

        self.threads_entry = tk.Entry(self.root)
        self.threads_entry.insert(0, str(self.max_threads))
        self.threads_entry.pack()

        convert_button = tk.Button(self.root, text="Convert", command=self.convert)
        convert_button.pack()

        self.root.mainloop()

    def browse_input(self):
        self.input_dir = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.input_dir)

    def browse_output(self):
        self.output_dir = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output_dir)

    def convert(self):
        self.max_threads = int(self.threads_entry.get())
        converter = Converter(self.input_dir, self.output_dir, self.max_threads)
        converter.convert_files()


if __name__ == "__main__":
    UX()
