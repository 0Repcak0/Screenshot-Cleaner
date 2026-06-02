import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

def file_hash(path, chunk_size=8192):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def scan(folder):
    folder = Path(folder)
    hashes = {}
    duplicates = []
    grouped = defaultdict(list)

    for file in folder.rglob("*"):
        if file.suffix.lower() not in IMAGE_EXTS:
            continue

        try:
            h = file_hash(file)
        except Exception:
            continue

        if h in hashes:
            duplicates.append((file, hashes[h]))
        else:
            hashes[h] = file

        date = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")
        grouped[date].append(file)

    return duplicates, grouped

def remove_duplicates(duplicates):
    for dup, _ in duplicates:
        try:
            dup.unlink()
            print(f"Deleted: {dup}")
        except Exception as e:
            print(f"Error deleting {dup}: {e}")

if __name__ == "__main__":
    folder = input("Path to screenshots folder: ")

    duplicates, grouped = scan(folder)

    print("\nDUPLICATES:")
    for d, o in duplicates:
        print(f"{d} -> {o}")

    print(f"\nFound {len(duplicates)} duplicates")

    if input("Delete duplicates? (y/n): ").lower() == "y":
        remove_duplicates(duplicates)

    print("\nGROUPED BY DATE:")
    for date, files in sorted(grouped.items()):
        print(date, len(files))