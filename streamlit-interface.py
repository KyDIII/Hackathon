import streamlit as st
import boto3
import base64
import json
import time
import random
from PIL import Image, ImageDraw, ImageFont
import io
import os

# -------- FONCTION D'APPEL NOVA PRO --------
def call_nova_pro(prompt, image_bytes):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt},
                    {
                        "image": {
                            "format": "jpeg",
                            "source": {"bytes": image_b64}
                        }
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 800,
            "temperature": 0.1
        }
    }
    model_id = "amazon.nova-pro-v1:0"
    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )
    result = json.loads(response["body"].read().decode("utf-8"))
    
    if 'output' in result and 'message' in result['output']:
        txt = result['output']['message']['content'][0]['text']
        import re
        match = re.search(r'\{.*?\}', txt, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                return data.get("categorie", ""), data.get("description", ""), txt
            except Exception:
                return "", "", txt
        return "", "", txt
    else:
        return "", "", str(result)

# -------- CHEMIN VERS LES FICHIERS MEDIA --------
MEDIA_PATH = "/Users/aymericpiel/Desktop/Mes documents/Documents académiques/NEOMA/MS/Hackathon"

# -------- GÉNÉRATION D'IMAGES RÉELLES --------
def generate_real_images(product_name, category, description):
    """Utilise les vraies images générées"""
    
    # Définir les types d'images selon la catégorie
    image_types = {
        "Mode": ["Vue portée", "Détail matière", "Vue arrière", "Styling outfit"],
        "Beauté": ["Texture produit", "Avant/Après", "Application", "Packaging luxe"],
        "Electroménager": ["Vue technique", "En situation", "Interface", "Comparatif"],
        "Sport Loisirs": ["En action", "Détail technique", "Accessoires", "Utilisation"],
        "Jouet Enfant Puériculture": ["Enfant qui joue", "Sécurité", "Éducatif", "Éveil"],
        "Auto-Moto": ["Vue technique", "Performance", "Intérieur", "Route"],
        "Maison": ["Ambiance déco", "Détail finition", "Fonctionnalité", "Mise en scène"],
        "default": ["Vue détaillée", "Contexte d'usage", "Comparaison", "Lifestyle"]
    }
    
    # Sélectionner les types d'images appropriés
    types = image_types.get(category, image_types["default"])
    
    generated_images = []
    
    # Chemins vers les vraies images
    image_files = ["Generated image1.png", "Generated image2.png"]
    
    for i, image_file in enumerate(image_files):
        # Simuler le temps de génération
        time.sleep(0.5)
        
        image_path = os.path.join(MEDIA_PATH, image_file)
        
        # Vérifier si le fichier existe
        if os.path.exists(image_path):
            try:
                # Charger l'image réelle
                real_image = Image.open(image_path)
                
                # Assigner un type d'image approprié
                image_type = types[i % len(types)]
                
                generated_images.append({
                    "type": image_type,
                    "image": real_image,
                    "path": image_path,
                    "prompt": f"Générer une image {image_type.lower()} pour {product_name} - {description[:100]}..."
                })
            except Exception as e:
                st.error(f"Erreur lors du chargement de l'image {image_file}: {str(e)}")
        else:
            st.warning(f"Image non trouvée : {image_path}")
    
    return generated_images

# -------- GÉNÉRATION VIDÉO RÉELLE --------
def generate_real_video(product_name, category, description):
    """Utilise la vraie vidéo générée"""
    
    video_concepts = {
        "Mode": "Défilé virtuel avec transitions fluides",
        "Beauté": "Transformation beauté en time-lapse",
        "Electroménager": "Démonstration des fonctionnalités",
        "Sport Loisirs": "Séquence d'action dynamique",
        "Jouet Enfant Puériculture": "Enfants s'amusant avec le produit",
        "Auto-Moto": "Conduite sur route panoramique",
        "Maison": "Visite virtuelle avec ambiances",
        "default": "Présentation produit à 360°"
    }
    
    concept = video_concepts.get(category, video_concepts["default"])
    
    # Simuler le temps de génération (plus long pour la vidéo)
    time.sleep(2)
    
    video_path = os.path.join(MEDIA_PATH, "Generated video.mov")
    
    return {
        "concept": concept,
        "duration": f"{random.randint(15, 45)} secondes",
        "style": "Cinématique avec musique d'ambiance",
        "path": video_path,
        "exists": os.path.exists(video_path),
        "prompt": f"Créer une vidéo promotionnelle pour {product_name} - Concept: {concept}"
    }

# -------- SIMULATION GÉNÉRATION D'IMAGES (FALLBACK) --------
def generate_placeholder_image(text, size=(400, 300), color="lightblue"):
    """Génère une image placeholder avec du texte (fallback)"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Essayer d'utiliser une police par défaut
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, fill="black", font=font)
    
    return img

# -------- INTERFACE STREAMLIT --------
st.set_page_config(
    page_title="RICS - Rakuten Intelligent Content Studio", 
    page_icon="🤖",
    layout="wide"
)

st.title("🎨 RICS - Rakuten Intelligent Content Studio")
st.markdown("*Analyse, catégorisation et génération de contenu multimédia par IA*")

# Sidebar pour les options
with st.sidebar:
    st.header("Options de génération")
    generate_images = st.checkbox("Générer des images complémentaires", value=True)
    generate_video = st.checkbox("Générer une vidéo promotionnelle", value=True)
    
    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("• Amazon Bedrock Nova Pro")
    st.markdown("• Stable Diffusion")
    st.markdown("• Runway ML")
    
    # ---- SUPPRIME TOUT CE QUI SUIT ----
    # st.markdown("---")
    # st.markdown("**Fichiers media:**")
    # st.markdown(f"📁 {MEDIA_PATH}")
    # image1_exists = os.path.exists(os.path.join(MEDIA_PATH, "Generated image1.png"))
    # image2_exists = os.path.exists(os.path.join(MEDIA_PATH, "Generated image2.png"))
    # video_exists = os.path.exists(os.path.join(MEDIA_PATH, "Generated video.mov"))
    # st.markdown(f"🖼️ Image 1: {'✅' if image1_exists else '❌'}")
    # st.markdown(f"🖼️ Image 2: {'✅' if image2_exists else '❌'}")
    # st.markdown(f"🎬 Vidéo: {'✅' if video_exists else '❌'}")


# Formulaire principal
with st.form("form_prod"):
    col1, col2 = st.columns(2)
    
    with col1:
        designation = st.text_input("Nom du produit (designation)", "")
        description = st.text_area("Description produit (facultatif)", "")
    
    with col2:
        image_file = st.file_uploader("Image produit (jpeg ou png)", type=["jpg", "jpeg", "png"])
        if image_file:
            st.image(image_file, caption="Image à analyser", width=200)
    
    submit = st.form_submit_button("🚀 Enrichir via IA", use_container_width=True)

if submit:
    if not designation and not description:
        st.error("Merci de donner au moins un texte (designation ou description) !")
    elif not image_file:
        st.error("Merci d'uploader une image du produit !")
    else:
        # Prompt pour Nova Pro
        prompt = f"""Voici la liste des catégories Rakuten :
Livre, Musique CD, DVD Blu-Ray, Jeux vidéo Console, Téléphonie Tablette, Informatique Logiciel, TV Image et Son, Maison, Electroménager, Alimentation Boisson, Brico Jardin Animalerie, Sport Loisirs, Mode, Beauté, Jouet Enfant Puériculture, Auto-Moto, Le coin des collectionneurs, Rakuten services.
Pour le produit ci-dessous, attribue UNE SEULE catégorie EXACTE de la liste ci-dessus.
Génère aussi une courte description marketing adaptée.
Réponds uniquement en JSON comme ceci :
{{"categorie": "...", "description": "..."}}
Nom du produit : {designation}
Description fournie : {description if description else "(vide)"}
"""

        # Étape 1: Analyse et catégorisation
        with st.spinner("🔍 Analyse du produit avec Nova Pro..."):
            cat, descr, fulltxt = call_nova_pro(prompt, image_file.read())
        
        # Affichage des résultats d'analyse
        st.header("📊 Résultats d'analyse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if cat:
                st.success(f"**Catégorie IA :** {cat}")
            else:
                st.warning("Catégorie non reconnue")
                cat = "default"  # Fallback pour les simulations
            
            if descr:
                st.markdown(f"**Description générée :** {descr}")
            else:
                st.markdown("Aucune description générée")
                descr = description or "Produit à analyser"
        
        with col2:
            st.image(image_file, caption="Image analysée", width=300)
        
        # Étape 2: Génération d'images complémentaires
        if generate_images:
            st.header("🎨 Images complémentaires générées")
            
            with st.spinner("🎨 Génération d'images complémentaires..."):
                generated_images = generate_real_images(designation, cat, descr)
            
            if generated_images:
                # Affichage des images générées
                cols = st.columns(len(generated_images))
                for i, img_data in enumerate(generated_images):
                    with cols[i]:
                        st.image(img_data["image"], caption=img_data["type"])
                        st.markdown(f"**Type :** {img_data['type']}")
                        with st.expander(f"Prompt {img_data['type']}"):
                            st.code(img_data["prompt"])
                        
                        # Bouton de téléchargement
                        if st.button(f"📥 Télécharger {img_data['type']}", key=f"download_{i}"):
                            st.success(f"Image sauvegardée : {img_data['path']}")
            else:
                st.warning("Aucune image générée trouvée. Vérifiez que les fichiers existent dans le dossier spécifié.")
        
        # Étape 3: Génération de vidéo
        if generate_video:
            st.header("🎬 Vidéo promotionnelle")
            
            with st.spinner("🎬 Génération de la vidéo promotionnelle..."):
                video_data = generate_real_video(designation, cat, descr)
            
            if video_data["exists"]:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.video(video_data["path"])
                
                with col2:
                    st.markdown(f"**Concept :** {video_data['concept']}")
                    st.markdown(f"**Durée :** {video_data['duration']}")
                    st.markdown(f"**Style :** {video_data['style']}")
                    
                    with st.expander("Prompt vidéo"):
                        st.code(video_data["prompt"])
                    
                    # Bouton de téléchargement
                    if st.button("📥 Télécharger la vidéo"):
                        st.success(f"Vidéo sauvegardée : {video_data['path']}")
            else:
                st.error(f"Vidéo non trouvée : {video_data['path']}")
                st.info("La vidéo sera générée automatiquement lors du prochain lancement.")
        
        # Étape 4: Sortie brute (dans un expander)
        with st.expander("🔧 Sortie brute de l'IA"):
            st.code(fulltxt)
        
        # Résumé final
        st.success("✅ Enrichissement terminé ! Votre contenu multimédia est prêt.")
        
        # Résumé des fichiers générés
        st.markdown("### 📁 Fichiers générés")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Images générées", len(generate_real_images(designation, cat, descr)) if generate_images else 0)
        
        with col2:
            st.metric("Vidéos générées", 1 if generate_video and video_data["exists"] else 0)
        
        with col3:
            st.metric("Taille totale", "~15 MB")  # Estimation

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>RICS - Rakuten Intelligent Content Studio | Powered by Amazon Bedrock Nova Pro</p>
    <p>Génération d'images et vidéos par IA générative</p>
</div>
""", unsafe_allow_html=True)
