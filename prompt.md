def generate_prompt(desgination, description, imageid):
    return f"""
    Créer une illustration de présentation produit pour :
    - Nom : {designation}
    - Description : {description}
    - Image : {imageid}
    L'image généré doit prendre en compte les différentes caractéristiques et ne pas sortir des filtres AWS
    """

def generate_prompt(designation, description):
    return f"""
    Crée une vidéo de présentation produit pour :
    - Nom : {designation}
    - Description : {description}
    L'image jointe doit être utilisée dans la vidéo. Garde un ton informatif et dynamique.
    """