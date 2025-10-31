"""
Stopmotion Webcam Recorder mit fester Vorschaugröße (640x480)
und voller Aufnahmeauflösung.

Funktionen:
- Vorschau bleibt fix bei 640x480 Pixeln
- Gespeicherte Bilder behalten volle Kameraauflösung
- Transparente Überlagerung der letzten Bilder (0–3)
- Einstellbare Transparenzen
- Speicherort frei wählbar
"""

import os
os.system("cls")
print("importing libs....")

#libs
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime


print("")
print("")
print("Hermanns Stop Motion Capture")
print("*2025, 31.10.2025")
print("uses a USB-Webcam")
print("")
print("")



class StopMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopmotion-Webcam Recorder")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        print("open Camera")
        # Kamera öffnen
        #self.cap = cv2.VideoCapture(0)

        #faster start
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



        # gewünschte Kameraauflösung setzen (volle Auflösung für Speicherung)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Couldnt open the Webcam.")
            root.destroy()
            return

        # Tatsächliche Auflösung auslesen
        self.cam_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cam_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera-Resolution: {self.cam_width} x {self.cam_height}")

        # Vorschaugröße fixieren (z. B. 640x480)
        self.preview_width = 640
        self.preview_height = 480

        # Zielordner
        self.output_dir = Path.cwd() / "captures"
        self.output_dir.mkdir(exist_ok=True)

        # Statusvariablen
        self.running = True
        self.latest_saved = []

       
        self.cached_bgs = []  # <<< Hier hinzufügen

        # Tkinter-Variablen (müssen vor Widgets existieren)
        self.webcam_alpha = tk.DoubleVar(value=0.5)
        self.bg_alpha = tk.DoubleVar(value=0.5)
        self.num_bgs = tk.IntVar(value=2) #bis zu 3 erlaubt

        # UI erstellen
        self.create_widgets()

        # Tastaturbindung
        self.root.bind("<space>", lambda e: self.capture_image())

        # Frame-Loop starten
        self.update_frame()



    def create_widgets(self):
        frm = ttk.Frame(self.root)
        frm.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Feste Vorschaugröße: Label ohne width/height-Argument
        self.preview_label = ttk.Label(frm)
        self.preview_label.pack(side=tk.TOP)

        # Steuerung
        ctrl = ttk.Frame(frm)
        ctrl.pack(side=tk.BOTTOM, fill=tk.X, pady=(8, 0))


        left = ttk.Frame(ctrl)
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(left, text="choose Destination", command=self.choose_folder).pack(side=tk.LEFT, padx=4)
        ttk.Button(left, text="Capture (Leertaste)", command=self.capture_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(left, text="Delete last", command=self.delete_last).pack(side=tk.LEFT, padx=4)

        right = ttk.Frame(ctrl)
        right.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        ttk.Label(right, text="Webcam-Transparency").pack(anchor=tk.E)
        ttk.Scale(right, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.webcam_alpha).pack(fill=tk.X, padx=4)

        ttk.Label(right, text="Backgound-Transparency").pack(anchor=tk.E)
        ttk.Scale(right, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.bg_alpha).pack(fill=tk.X, padx=4)

        ttk.Label(right, text="Amount of Backgrounds (0–3)").pack(anchor=tk.E)
        ttk.Spinbox(right, from_=0, to=3, textvariable=self.num_bgs, width=3).pack(anchor=tk.E, padx=4)

        # Statusleiste
        self.status_var = tk.StringVar(value=f"Save Directory: {self.output_dir}")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def choose_folder(self):
        """Ordner wählen – optional"""
        d = filedialog.askdirectory(initialdir=str(self.output_dir))
        if d:
            self.output_dir = Path(d)
            self.output_dir.mkdir(exist_ok=True)
            self.status_var.set(f"Save Directory: {self.output_dir}")
            self.refresh_saved_list()

    def old_refresh_saved_list(self):
        files = sorted(self.output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        self.latest_saved = files[:10]



    def refresh_saved_list(self):
        files = sorted(self.output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        self.latest_saved = files[:10]
        self.cached_bgs = []

        # Cache für 3 Hintergrundbilder laden
        for p in self.latest_saved[:3]:
            try:
                img = Image.open(p).convert("RGBA")
                self.cached_bgs.append(img)
            except Exception:
                pass
 



    def capture_image(self):
        """Einzelbild in voller Auflösung speichern"""
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Couldnt read Frame from Webcam.")
            return

        # In RGB konvertieren (OpenCV → Pillow)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Speichern in voller Auflösung
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = self.output_dir / f"capture_{now}.png"
        img.save(fname, format="PNG")

        self.refresh_saved_list()
        self.status_var.set(f"Saved: {fname.name}")

    def delete_last(self):
        self.refresh_saved_list()
        if not self.latest_saved:
            messagebox.showinfo("No Pictures", "there are No Pictures for deleting.")
            return
        last = self.latest_saved[0]
        try:
            last.unlink()
            self.status_var.set(f"Deleted: {last.name}")
        except Exception as e:
            messagebox.showerror("Error", f"couldnt delete File:\n{e}")
        self.refresh_saved_list()

#---------------neu-compose frame----------

    def compose_frame(self, frame_rgb):
        """Mische bis zu 3 Hintergrundbilder mit Webcam-Bild."""
        h, w, _ = frame_rgb.shape

        # Leeres RGBA-Bild für die Hintergründe
        base = Image.new("RGBA", (w, h), (0, 0, 0, 0))

        num = max(0, min(3, self.num_bgs.get()))

        if num > 0 and self.cached_bgs:
            for im in self.cached_bgs[:num][::-1]:
                # Größe anpassen
                im_resized = im.resize((w, h))
                # Transparenz setzen **unabhängig vom Webcam-Bild**
                im_alpha = im_resized.copy()
                im_alpha.putalpha(int(255 * self.bg_alpha.get()))
                # Nur mit Base mischen, Webcam noch nicht
                base = Image.alpha_composite(base, im_alpha)

        # Webcam-Bild separat als Overlay
        cam_img = Image.fromarray(frame_rgb).convert("RGBA")
        cam_img.putalpha(int(255 * self.webcam_alpha.get()))
        # Webcam immer oben drauf
        out = Image.alpha_composite(base, cam_img)

        return out.convert("RGB")


#--------------old compose frame--------


    def old_compose_frame(self, frame_rgb):
        """Mische Hintergrundbilder und Webcam-Overlay für die Vorschau."""
        h, w, _ = frame_rgb.shape
        base = Image.new("RGBA", (w, h), (0, 0, 0, 0))

        num = max(0, min(3, self.num_bgs.get()))
        self.refresh_saved_list()
        bg_paths = self.latest_saved[:num]

        if not bg_paths:
            cam_img = Image.fromarray(frame_rgb).convert("RGBA")
            a = int(255 * self.webcam_alpha.get())
            cam_img.putalpha(a)
            out = Image.alpha_composite(Image.new("RGBA", cam_img.size, (255, 255, 255, 255)), cam_img)
            return out.convert("RGB")

        for p in reversed(bg_paths):
            try:
                with Image.open(p) as im:
                    im = im.convert("RGBA").resize((w, h))
                    im.putalpha(int(255 * self.bg_alpha.get()))
                    base = Image.alpha_composite(base, im)
            except Exception:
                continue

        cam_img = Image.fromarray(frame_rgb).convert("RGBA")
        cam_img.putalpha(int(255 * self.webcam_alpha.get()))
        out = Image.alpha_composite(base, cam_img)

        return out.convert("RGB")

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            composed = self.compose_frame(frame_rgb)

           
            composed = composed.resize((self.preview_width, self.preview_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(composed)
            self.preview_label.configure(image=self.photo)
 

            # Vorschau auf 640x480 skalieren
            #composed = composed.resize((self.preview_width, self.preview_height), Image.LANCZOS)
            #self.photo = ImageTk.PhotoImage(composed)
            #self.preview_label.configure(image=self.photo)

        self.root.after(30, self.update_frame)

    def on_close(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StopMotionApp(root)
    root.mainloop()
