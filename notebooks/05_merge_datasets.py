import os
import shutil
from pathlib import Path

# ─── PATHS ───────────────────────────────────────────────────────────────────
BASE = Path(r"A:\AgriIntel_Project\AgriIntel\datasets")

SRC_PLANTVILLAGE = BASE / "plantvillage"
SRC_PLANTDOC_TRAIN = BASE / "plantdoc" / "PlantDoc-Dataset-master" / "PlantDoc-Dataset-master" / "train"
SRC_PLANTDOC_TEST  = BASE / "plantdoc" / "PlantDoc-Dataset-master" / "PlantDoc-Dataset-master" / "test"
SRC_RICE     = BASE / "rice_field"    / "Rice"
SRC_WHEAT    = BASE / "wheat_field"   / "Wheat" / "Wheat Disease Dataset"
SRC_SUGARCANE_DIS = BASE / "sugarcane_field" / "Sugarcane Disease Dataset" / "Diseases"
SRC_SUGARCANE_HLT = BASE / "sugarcane_field" / "Sugarcane Disease Dataset" / "Healthy Leaves"

OUTPUT = BASE / "unified_dataset"

# ─── PLANTDOC → PLANTVILLAGE CLASS MAPPING ───────────────────────────────────
PLANTDOC_MAP = {
    "Apple leaf":                           "Apple___healthy",
    "Apple rust leaf":                      "Apple___Cedar_apple_rust",
    "Apple Scab Leaf":                      "Apple___Apple_scab",
    "Bell_pepper leaf":                     "Pepper,_bell___healthy",
    "Bell_pepper leaf spot":                "Pepper,_bell___Bacterial_spot",
    "Blueberry leaf":                       "Blueberry___healthy",
    "Cherry leaf":                          "Cherry_(including_sour)___healthy",
    "Corn Gray leaf spot":                  "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn leaf blight":                     "Corn_(maize)___Northern_Leaf_Blight",
    "Corn rust leaf":                       "Corn_(maize)___Common_rust_",
    "grape leaf":                           "Grape___healthy",
    "grape leaf black rot":                 "Grape___Black_rot",
    "Peach leaf":                           "Peach___healthy",
    "Potato leaf early blight":             "Potato___Early_blight",
    "Potato leaf late blight":              "Potato___Late_blight",
    "Raspberry leaf":                       "Raspberry___healthy",
    "Soyabean leaf":                        "Soybean___healthy",
    "Squash Powdery mildew leaf":           "Squash___Powdery_mildew",
    "Strawberry leaf":                      "Strawberry___healthy",
    "Tomato Early blight leaf":             "Tomato___Early_blight",
    "Tomato leaf":                          "Tomato___healthy",
    "Tomato leaf bacterial spot":           "Tomato___Bacterial_spot",
    "Tomato leaf late blight":              "Tomato___Late_blight",
    "Tomato leaf mosaic virus":             "Tomato___Tomato_mosaic_virus",
    "Tomato leaf yellow virus":             "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato mold leaf":                     "Tomato___Leaf_Mold",
    "Tomato Septoria leaf spot":            "Tomato___Septoria_leaf_spot",
    "Tomato two spotted spider mites leaf": "Tomato___Spider_mites Two-spotted_spider_mite",
}

# ─── RICE FIELD → TARGET CLASS MAPPING ───────────────────────────────────────
RICE_MAP = {
    "Bacterialblight": "Rice___Bacterial_Leaf_Blight",
    "Blast":           "Rice___Leaf_Blast",
    "Brownspot":       "Rice___Brown_Spot",
    "Tungro":          "Rice___Tungro",
}

# ─── WHEAT FIELD → TARGET CLASS MAPPING ──────────────────────────────────────
WHEAT_MAP = {
    "BrownRust":  "Wheat___Brown_rust",
    "Healthy":    "Wheat___Healthy",
    "Mildew":     "Wheat___Mildew",
    "Septoria":   "Wheat___septoria",
    "YellowRust": "Wheat___stripe_rust",
}

# ─── SUGARCANE → NEW CLASS MAPPING ───────────────────────────────────────────
SUGARCANE_DIS_MAP = {
    "BrownRust":  "Sugarcane___Brown_rust",
    "Mawa":       "Sugarcane___Grassy_shoot",
    "Mites":      "Sugarcane___Mites",
    "RedSpot":    "Sugarcane___Red_spot",
    "YellowLeaf": "Sugarcane___Yellow_leaf",
}
SUGARCANE_HLT_TARGET = "Sugarcane___healthy"


# ─── HELPER: copy all images from src_folder into output_class_folder ─────────
def copy_images(src_folder: Path, target_class: str, prefix: str):
    """
    Copies all .jpg/.jpeg/.png images from src_folder into
    OUTPUT/target_class/, renaming each file as prefix_originalname
    to avoid collisions between datasets.
    """
    dest = OUTPUT / target_class
    dest.mkdir(parents=True, exist_ok=True)

    if not src_folder.exists():
        print(f"  [SKIP] Source not found: {src_folder}")
        return 0

    count = 0
    for img in src_folder.iterdir():
        if img.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            new_name = f"{prefix}_{img.name}"
            dest_file = dest / new_name
            # If file already exists (very unlikely with prefix), add counter
            counter = 0
            while dest_file.exists():
                counter += 1
                dest_file = dest / f"{prefix}_{counter}_{img.name}"
            shutil.copy2(img, dest_file)
            count += 1
    return count


# ─── STEP 1: Copy all PlantVillage classes as-is ─────────────────────────────
print("=" * 60)
print("STEP 1: Copying PlantVillage...")
pv_total = 0
for class_folder in sorted(SRC_PLANTVILLAGE.iterdir()):
    if class_folder.is_dir():
        n = copy_images(class_folder, class_folder.name, "pv")
        print(f"  {class_folder.name}: {n} images")
        pv_total += n
print(f"PlantVillage total: {pv_total} images\n")


# ─── STEP 2: Merge PlantDoc (train + test) ───────────────────────────────────
print("=" * 60)
print("STEP 2: Merging PlantDoc...")
pd_total = 0
for split_folder in [SRC_PLANTDOC_TRAIN, SRC_PLANTDOC_TEST]:
    split_name = split_folder.name  # "train" or "test"
    if not split_folder.exists():
        print(f"  [SKIP] {split_folder} not found")
        continue
    for class_folder in sorted(split_folder.iterdir()):
        if class_folder.is_dir():
            plantdoc_class = class_folder.name
            if plantdoc_class in PLANTDOC_MAP:
                target = PLANTDOC_MAP[plantdoc_class]
                n = copy_images(class_folder, target, f"pd_{split_name}")
                print(f"  {plantdoc_class} → {target}: {n} images")
                pd_total += n
            else:
                print(f"  [UNMAPPED] {plantdoc_class} — skipping")
print(f"PlantDoc total: {pd_total} images\n")


# ─── STEP 3: Merge Rice field dataset ────────────────────────────────────────
print("=" * 60)
print("STEP 3: Merging Rice field dataset...")
rice_total = 0
for folder_name, target_class in RICE_MAP.items():
    src = SRC_RICE / folder_name
    n = copy_images(src, target_class, "rf")
    print(f"  {folder_name} → {target_class}: {n} images")
    rice_total += n
print(f"Rice field total: {rice_total} images\n")


# ─── STEP 4: Merge Wheat field dataset ───────────────────────────────────────
print("=" * 60)
print("STEP 4: Merging Wheat field dataset...")
wheat_total = 0
for folder_name, target_class in WHEAT_MAP.items():
    src = SRC_WHEAT / folder_name
    n = copy_images(src, target_class, "wf")
    print(f"  {folder_name} → {target_class}: {n} images")
    wheat_total += n
print(f"Wheat field total: {wheat_total} images\n")


# ─── STEP 5: Merge Sugarcane disease classes ─────────────────────────────────
print("=" * 60)
print("STEP 5: Merging Sugarcane...")
sc_total = 0
for folder_name, target_class in SUGARCANE_DIS_MAP.items():
    src = SRC_SUGARCANE_DIS / folder_name
    n = copy_images(src, target_class, "sc")
    print(f"  {folder_name} → {target_class}: {n} images")
    sc_total += n

# Sugarcane healthy is at a different path
n = copy_images(SRC_SUGARCANE_HLT, SUGARCANE_HLT_TARGET, "sc")
print(f"  Healthy Leaves → {SUGARCANE_HLT_TARGET}: {n} images")
sc_total += n
print(f"Sugarcane total: {sc_total} images\n")


# ─── FINAL SUMMARY ───────────────────────────────────────────────────────────
print("=" * 60)
print("MERGE COMPLETE. Summary:")
all_classes = sorted(OUTPUT.iterdir())
grand_total = 0
for cls in all_classes:
    if cls.is_dir():
        count = len(list(cls.glob("*")))
        print(f"  {cls.name}: {count} images")
        grand_total += count
print(f"\nTotal classes: {len(all_classes)}")
print(f"Total images:  {grand_total}")
print(f"Output folder: {OUTPUT}")