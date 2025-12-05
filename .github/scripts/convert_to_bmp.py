import os
from pathlib import Path
from PIL import Image

# Dossiers source (PNG/JPG/etc.) et destination (BMP)
SRC_DIR = Path("source-logos")
DST_DIR = Path("logos")

# Taille cible optionnelle (None = ne pas redimensionner)
# Si tu veux que tout tienne dans ~16 px de haut sur ta matrice :
TARGET_HEIGHT = 16

# Extensions d'entrée acceptées
VALID_EXT = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")


def convert_one(src_path: Path, dst_path: Path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(src_path).convert("RGB")  # BMP = pas de transparence

    if TARGET_HEIGHT is not None:
        w, h = img.size
        if h != TARGET_HEIGHT:
            new_w = int(w * TARGET_HEIGHT / h)
            img = img.resize((new_w, TARGET_HEIGHT), Image.LANCZOS)

    # Forcer BMP
    dst_path = dst_path.with_suffix(".bmp")
    img.save(dst_path, format="BMP")
    print(f"Converti: {src_path} -> {dst_path}")


def main():
    if not SRC_DIR.exists():
        print(f"{SRC_DIR} n'existe pas, rien à faire.")
        return

    for root, dirs, files in os.walk(SRC_DIR):
        for name in files:
            if not name.lower().endswith(VALID_EXT):
                continue

            src_path = Path(root) / name
            rel = src_path.relative_to(SRC_DIR)
            dst_path = DST_DIR / rel

            convert_one(src_path, dst_path)


if __name__ == "__main__":
    main()
