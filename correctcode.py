import html
import os

def convertir_caracteres_speciaux(input_path, output_path):
    """
    Convertit les caractères spéciaux en entités HTML dans un fichier donné.

    Args:
        input_path (str): Chemin du fichier d'entrée.
        output_path (str): Chemin du fichier de sortie.
    """
    try:
        # Lire le contenu du fichier d'entrée
        with open(input_path, "r", encoding="utf-8") as file:
            contenu = file.read()
        
        # Convertir les caractères spéciaux en entités HTML
        contenu_converti = html.escape(contenu, quote=True)
        
        # Remplacement manuel pour les apostrophes et guillemets
        contenu_converti = contenu_converti.replace("'", "&rsquo;").replace('"', "&quot;")
        
        # Ajouter une mention à Informaclique.fr
        mention = "\n<!-- Converti par Informaclique.fr -->\n"
        contenu_converti += mention

        # Écrire le contenu converti dans le fichier de sortie
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(contenu_converti)
        
        print(f"\n✅ Conversion réussie !")
        print(f"Le fichier converti a été sauvegardé sous : {output_path}")
        print("Merci d'utiliser Informaclique.fr 🚀")
    except Exception as e:
        print(f"\n❌ Erreur lors de la conversion : {e}")

def afficher_menu():
    """
    Affiche un menu interactif pour demander le chemin du fichier à convertir.
    """
    print("===================================")
    print("🎉 Bienvenue dans l'outil de conversion HTML 🎉")
    print("      Développé par Informaclique.fr")
    print("===================================")
    
    # Demander le chemin du fichier d'entrée
    input_path = input("\n📂 Entrez le chemin complet du fichier HTML à convertir : ").strip()
    if not os.path.exists(input_path):
        print("\n❌ Le fichier spécifié n'existe pas. Veuillez vérifier le chemin.")
        return

    # Générer automatiquement le chemin du fichier de sortie
    output_path = input_path.replace(".html", "_converti.html")
    
    # Lancer la conversion
    convertir_caracteres_speciaux(input_path, output_path)

# Lancer le menu interactif
if __name__ == "__main__":
    afficher_menu()
