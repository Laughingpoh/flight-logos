from pathlib import Path
from PIL import Image

SRC_DIR = Path("source-logos")
DST_DIR = Path("logos")
TARGET_SIZE = 16  # Taille des logos pour l’écran Matrix Portal S3

DST_DIR.mkdir(exist_ok=True)

print("Conversion des logos vers BMP 8-bit palette...")

for src in SRC_DIR.iterdir():
    if not src.is_file():
        continue

    try:
        img = Image.open(src).convert("RGBA")
    except Exception as e:
        print("❌ Erreur ouverture", src, ":", e)
        continue

    w, h = img.size

    # --- Redimensionnement avec respect du ratio ---
    scale = TARGET_SIZE / float(max(w, h))
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # --- Création image carrée 16×16 ---
    bg = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))

    # Centrage
    offset_x = (TARGET_SIZE - new_w) // 2
    offset_y = (TARGET_SIZE - new_h) // 2
    bg.paste(img, (offset_x, offset_y), img)

    # --- Conversion palette (nécessaire pour CircuitPython) ---
    # 64 couleurs = largement suffisant pour des logos 16×16
    pal = bg.convert("P", palette=Image.ADAPTIVE, colors=64)

    # --- Nom de sortie en UPPERCASE pour correspondre aux ICAO/IATA ---
    dst_name = src.stem.upper() + ".bmp"
    dst_path = DST_DIR / dst_name

    try:
        pal.save(dst_path, format="BMP")
        print(f"✅ {src.name} → {dst_name}")
    except Exception as e:
        print("❌ Erreur sauvegarde", dst_path, ":", e)

print("Terminé 👍")
