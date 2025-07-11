import os
import json
import base64
import boto3
import pandas as pd
import re
from pathlib import Path

# === CONFIGURATION ===
CSV_PATH = "/Users/victor/Documents/Documents - MacBook Air de Victor/PARA/01. PROJECTS/Hackathon/X_train_update.csv"
OUTPUT_FOLDER = "outputs"
MODEL_ID = "amazon.titan-image-generator-v1"
REGION = "us-west-2"

# Initialisation Bedrock
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

# Fonction de nettoyage du prompt
def sanitize_prompt(prompt: str) -> str:
    # Suppression caractères spéciaux
    prompt = re.sub(r'[^\w\s\.,]', '', prompt)
    prompt = re.sub(r'\s+', ' ', prompt).strip()

    # Liste noire de mots filtrés
    blocked_words = [
        "playstation", "diablo", "mtv", "louvre", "schtroumpf", "sony",
        "gta", "warner", "bac", "examens", "guerre", "armes", "nazi", "porno",
        "kill", "attaque", "honte", "interventions", "hacker", "terror", "dark"
    ]
    for word in blocked_words:
        prompt = re.sub(fr"\b{word}\b", "", prompt, flags=re.IGNORECASE)

    # Nettoyage final
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    return prompt[:512]


# Charger les données
df = pd.read_csv(CSV_PATH)
df = df.head(50)  # pour test initial

# Génération
for index, row in df.iterrows():
    imageid = str(row['imageid'])
    productid = str(row['productid'])
    designation = str(row['designation']) if pd.notna(row['designation']) else ""
    description = str(row['description']) if pd.notna(row['description']) else ""

    # Générer et nettoyer le prompt
    raw_prompt = f"Créer une image représentant le produit suivant : '{designation}'. Description : {description}"
    prompt = sanitize_prompt(raw_prompt)

    output_path = os.path.join(OUTPUT_FOLDER, f"titan_{imageid}_{productid}.png")
    if os.path.exists(output_path):
        print(f"[SKIP] Déjà générée : {output_path}")
        continue

    body = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "height": 512,
            "width": 512,
            "cfgScale": 8.0,
            "seed": 42
        }
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response['body'].read())
        image_b64 = result['images'][0]
        image_bytes = base64.b64decode(image_b64)

        with open(output_path, "wb") as out_file:
            out_file.write(image_bytes)

        print(f"[OK] Image générée : {output_path}")

    except Exception as e:
        print(f"[ERREUR] {productid} → {e}")
