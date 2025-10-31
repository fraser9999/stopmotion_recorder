# StopMotion-Webcam Recorder

Ein **Python-basiertes Stopmotion-Aufnahme-Tool** mit USB-Webcam.  
Es bietet eine **Live-Vorschau**, die bis zu **3 vorherige Einzelbilder transparent überlagert**, und ermöglicht die **Aufnahme in voller Kameraauflösung**.

## Features

- Aufnahme von Einzelbildern per **Leertaste** oder Button  
- Vorschau in **640×480 Pixel** (stabile Größe)  
- Gespeicherte Bilder in **voller Kameraauflösung**  
- Bis zu **3 Hintergrundbilder** als transparente Referenz  
- Transparenz der Webcam und der Hintergrundbilder über **Slider einstellbar**  
- Ordnerwahl für gespeicherte Bilder  
- Löschfunktion für das zuletzt gespeicherte Bild  
- Schneller Start über DirectShow (Windows)


## Voraussetzungen

- Python 3.10+  
- Windows (optimal für DirectShow; unter Linux können kleine Anpassungen nötig sein)  
- USB-Webcam (Logitech empfohlen, aber jede UVC-kompatible Kamera funktioniert)  

### Benötigte Python-Pakete

```bash
pip install opencv-python Pillow
