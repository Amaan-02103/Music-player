import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
from mutagen.mp3 import MP3

class AdvancedMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaana Bajao")
        self.root.geometry("400x320")
        self.root.configure(bg="black")
        self.root.resizable(0,0)

        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()
        self.duration = 0
        self.current_time = 0

        self.create_ui()

    def create_ui(self):
        # Track information
        track_frame = tk.LabelFrame(self.root, text="Track", font=("times new roman", 15, "bold"), bg="#777a7d", fg="white", bd=5, relief=tk.GROOVE)
        track_frame.place(x=0, y=0, width=400, height=100)

        song_track = tk.Label(track_frame, textvariable=self.track, width=30, font=("times new roman", 12, "bold"), bg="#777a7d", fg="white")
        song_track.grid(row=0, column=0, padx=10, pady=5)

        track_status = tk.Label(track_frame, textvariable=self.status, font=("times new roman", 12, "bold"), bg="#777a7d", fg="white")
        track_status.grid(row=1, column=0, padx=10, pady=5)

        # Button frame
        button_frame = tk.LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), bg="#585a5c", fg="white", bd=5, relief=tk.GROOVE)
        button_frame.place(x=0, y=100, width=400, height=120)

        play_btn = tk.Button(button_frame, text="PLAY", command=self.play_music, width=6, height=1, font=("times new roman", 12, "bold"), fg="white", bg="#27ae60")
        play_btn.grid(row=0, column=0, padx=10, pady=5)

        pause_btn = tk.Button(button_frame, text="PAUSE", command=self.pause_music, width=8, height=1, font=("times new roman", 12, "bold"), fg="white", bg="#2980b9")
        pause_btn.grid(row=0, column=1, padx=10, pady=5)

        stop_btn = tk.Button(button_frame, text="STOP", command=self.stop_music, width=6, height=1, font=("times new roman", 12, "bold"), fg="white", bg="#c0392b")
        stop_btn.grid(row=0, column=2, padx=10, pady=5)

        load_btn = tk.Button(button_frame, text="LOAD", command=self.load_music, width=6, height=1, font=("times new roman", 12, "bold"), fg="white", bg="#8e44ad")
        load_btn.grid(row=0, column=3, padx=10, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(button_frame, length=360, mode='determinate')
        self.progress.grid(row=1, columnspan=4, padx=10, pady=10)

        # Volume control
        volume_frame = tk.LabelFrame(self.root, text="Volume", font=("times new roman", 15, "bold"), bg="#38393b", fg="white", bd=5, relief=tk.GROOVE)
        volume_frame.place(x=0, y=220, width=400, height=100)

        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume, length=370)
        self.volume_slider.set(0.5)  # Set default volume
        pygame.mixer.music.set_volume(0.5)
        self.volume_slider.grid(row=0, column=0, padx=10, pady=20)

    def load_music(self):
        self.music_file = filedialog.askopenfilename()
        self.track.set(os.path.basename(self.music_file))
        self.status.set("Ready")
        self.duration = MP3(self.music_file).info.length

    def play_music(self):
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()
            self.status.set("Playing")
            self.update_progress()

    def pause_music(self):
        if self.status.get() == "Playing":
            pygame.mixer.music.pause()
            self.status.set("Paused")
        elif self.status.get() == "Paused":
            pygame.mixer.music.unpause()
            self.status.set("Playing")
            self.update_progress()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped")
        self.progress['value'] = 0

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def update_progress(self):
        if self.status.get() == "Playing":
            self.current_time = pygame.mixer.music.get_pos() / 1000
            self.progress['value'] = (self.current_time / self.duration) * 100
            self.root.after(1000, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    player = AdvancedMusicPlayer(root)
    root.mainloop()
