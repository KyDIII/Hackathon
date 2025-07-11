import os
import pandas as pd
import requests

# Configuration
CSV_PATH = "/Users/victor/Documents/Documents - MacBook Air de Victor/PARA/01. PROJECTS/Hackathon/X_train_update.csv"
IMAGE_DIR = "/Users/victor/Documents/Documents - MacBook Air de Victor/PARA/01. PROJECTS/Hackathon/images/image_train"
NOVA_API_KEY = "export AWS_BEARER_TOKEN_BEDROCK=bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUFRRkNDVkIyQlZaUENZWUhJJTJGMjAyNTA3MTElMkZ1cy1lYXN0LTElMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA3MTFUMDg0MzI4WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFTW4lMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RWFDWFZ6TFdWaGMzUXRNU0pITUVVQ0lRRENVNmp1Q2NQZndKSyUyQkxEU05jTXpvbkdGc081alBvb3lvQU5KRTR0b2l6Z0lnZnI1bzB5cEFpcHdyVTFaUnJsZDNCbiUyRnpoR0ZUMWhaeVhXYXhCbFFGQnU0cXZRTUkwdiUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRiUyRkFSQUJHZ3d3TVRBNE56Y3lNVEF5TkRNaURDZXdYVkFsblY5c3VVVDgyaXFSQXdRY0ZJNWNzY01nZVV1UjJ0b3ZsQUpwTnBJR3lvekVYQkxRcVBrQ1BpbE9qRGRYRlZ6TTF6dTRCOENCaU1aOFZjayUyQmVyb2IlMkZhckFJVUVlZUNjamFpZEp1SGR4WFN5a1FOUDBwVUclMkZOUHVhbEVob1hmQjc3QWV6eDhib1dqZ1BEeE9GVFpxbk9nREZJWjI4UFVTeXpWc2h0RHJqeXJPNiUyQlBWSnclMkZsODR1SE1PNFhTY0o2dSUyRkhORzJ6U2N1b0JrYk02SVE1bm1oUFR4Y3FUcWlGJTJCRkJreVFlYVNoRUhYJTJCQjZsUWNSZWtNb0NQWjI4U3VBVjJZdyUyQmVRMTFDUmdqc1lTRm9NakhiYnhTZDQ1d3ZlQmVjUTZaN1VkUUhSa2hsMnNlY0Jma2V3VEhXeGl6RHYlMkJLTG96N09JbVJERTNJTlFjV0lUNlBpandwWEVrcFpGUm01UkJLUmRtVzU4SUtqNXNiczdmTVlhbU91NnFHcHJmYzBCUmJaZlphOFEyVmpFem13dFc0QmpWcXF5SVFEVmFwSmVnY042RXlidkhhZ0NjNUNHMWtBY1Nsam5wMjM3Q2NRbmRHSVh5R3JkUFpCN2slMkZoUm9LeEx6OEdndktjWEUyOW84JTJCSDZYS1hHejBka3VvM2JPVE5YdHZKcCUyRkJNanZDUFBhMGVTYWpacSUyQlJxaVhNa0tzM1dKNHN1TGdKUE5PdmNmeUo1TUtLRnc4TUdPcmNDVW9aWE5PSmY1eWVwak13STU0ZjdoT3NtNmFERjFmJTJGZU4yTVBweU5mbnFpTXJzdHI0ZGdaNjNDU1FXN1E1QWpjWmlpU1glMkZON3d2WlpyM0tUbVBwWlpzTXRaVUFWUUZoTnFxM2wzV0dSbjNlcG9wR2xSbkNVbU8lMkZkOUoxR01za212Z1N2ckJ0TUtjRWhMV2JUZWZybGxzNWdDM3YwV3JoazAxQ3BsNUVORjluSFklMkZnbERqUlBTNllaRzJRYkx4dll0MGE0VDFqJTJGcDNTZyUyQlVkdkJCTUc0NjdFNDR0RDNTeDdTN0p5S1IlMkJEJTJCVEhtJTJCb3VqV0VZbXB5UFVIVG5kWUlrSmk5bCUyRjBHNDl5Tkp2QXhrVjRRYkRhRXkzMmNzdUFvWXF2UWtEcHYwOWsyVWJxaFhPZnZUWGd2d0daTlczOEkyTjZrYmJvSnFSSGhQbWU0cVVDTGpUbGNUWVNCdlFHZngzVTQ2Z1dpU0FSaWptaE1DNkdFcDl2VzEwVjZUanh2SUdNQ2h0ZHg5Y3RIejBxTWpQWEx2c1hvdFR5UHhTQyUyQnclM0QmWC1BbXotU2lnbmF0dXJlPWU5ZGM5NzQ0MWYyYjlhMzJhY2UwNzEwODM1NTUzMGU0NDYyMmJhMTUwNzg4Y2JhZDM0NTVlNTg5ZTJhODU0Y2QmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JlZlcnNpb249MQ=="
NOVA_API_URL = "https://api.novareel.ai/v1/generate_video"
HEADERS = {"Authorization": f"Bearer {NOVA_API_KEY}"}

# Charger les données
df = pd.read_csv(CSV_PATH)
df = df.dropna(subset=["description"])

def get_image_filename(imageid, productid):
    return f"image_{int(imageid)}_product_{int(productid)}.jpg"

def generate_prompt(designation, description):
    return f"""
    Crée une vidéo de présentation produit pour :
    - Nom : {designation}
    - Description : {description}
    L'image jointe doit être utilisée dans la vidéo. Garde un ton informatif et dynamique.
    """

# Résultats
results = []

for _, row in df.iterrows():
    designation = row['designation']
    description = row['description']
    imageid = row['imageid']
    productid = row['productid']

    image_filename = get_image_filename(imageid, productid)
    image_path = os.path.join(IMAGE_DIR, image_filename)

    if not os.path.exists(image_path):
        print(f"[⚠️] Image introuvable pour {designation}")
        continue

    prompt = generate_prompt(designation, description)
    
    # Requête vers NovaReel
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            NOVA_API_URL,
            headers=HEADERS,
            data={"prompt": prompt},
            files={"image": image_file}
        )

    if response.status_code == 200:
        video_url = response.json().get("video_url", "N/A")
        print(f"[✅] Vidéo OK pour {designation}")
        results.append({"productid": productid, "video_url": video_url})
    else:
        print(f"[❌] Échec pour {designation} : {response.text}")
        results.append({"productid": productid, "video_url": None})

# Sauvegarde des résultats
result_df = pd.DataFrame(results)
result_df.to_csv("videos_generées.csv", index=False)
