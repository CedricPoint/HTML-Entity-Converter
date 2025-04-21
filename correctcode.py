import html
import os
import json
import logging
import webbrowser
import tempfile
from typing import Dict, Optional, List, Tuple
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel

# Configuration avancée
CONFIG_FILE = "converter_config.json"
console = Console()

# Configuration du logging avec rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.RotatingFileHandler('conversion_log.txt', maxBytes=1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)

# Dictionnaire étendu des caractères spéciaux
CARACTERES_SPECIAUX: Dict[str, str] = {
    # Lettres accentuées françaises
    "à": "&agrave;", "â": "&acirc;", "ä": "&auml;", "é": "&eacute;",
    "è": "&egrave;", "ê": "&ecirc;", "ë": "&euml;", "î": "&icirc;",
    "ï": "&iuml;", "ô": "&ocirc;", "ö": "&ouml;", "ù": "&ugrave;",
    "û": "&ucirc;", "ü": "&uuml;", "ÿ": "&yuml;", "ç": "&ccedil;",
    
    # Symboles courants
    "œ": "&oelig;", "Œ": "&OElig;", "æ": "&aelig;", "Æ": "&AElig;",
    "€": "&euro;", "£": "&pound;", "¥": "&yen;", "©": "&copy;",
    "®": "&reg;", "™": "&trade;", "°": "&deg;", "±": "&plusmn;",
    "×": "&times;", "÷": "&divide;", "¼": "&frac14;", "½": "&frac12;",
    "¾": "&frac34;", "²": "&sup2;", "³": "&sup3;", "¹": "&sup1;",
    
    # Ponctuation et espaces
    "«": "&laquo;", "»": "&raquo;", "‹": "&lsaquo;", "›": "&rsaquo;",
    "—": "&mdash;", "–": "&ndash;", "…": "&hellip;", " ": "&nbsp;",
    "¡": "&iexcl;", "¿": "&iquest;",
    
    # Symboles mathématiques
    "∑": "&sum;", "∏": "&prod;", "∂": "&part;", "∞": "&infin;",
    "∫": "&int;", "≈": "&asymp;", "≠": "&ne;", "≤": "&le;",
    "≥": "&ge;", "⊂": "&sub;", "⊃": "&sup;"
}

class Configuration:
    """Gestion des préférences utilisateur"""
    def __init__(self):
        self.config_path = Path(CONFIG_FILE)
        self.default_config = {
            "mode_strict": False,
            "backup_files": True,
            "preview_before_save": True,
            "max_workers": 4,
            "default_output_dir": "converted_files",
            "custom_entities": {}
        }
        self.current_config = self.charger_config()

    def charger_config(self) -> dict:
        """Charge la configuration depuis le fichier"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.default_config, **json.load(f)}
            except Exception as e:
                logging.warning(f"Erreur lors du chargement de la configuration: {e}")
        return self.default_config.copy()

    def sauvegarder_config(self) -> None:
        """Sauvegarde la configuration actuelle"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la configuration: {e}")

class ConvertisseurHTML:
    def __init__(self):
        self.stats = {
            "caracteres_convertis": 0,
            "fichiers_traites": 0,
            "erreurs": 0,
            "temps_total": 0.0
        }
        self.config = Configuration()
        self.caracteres_speciaux = {**CARACTERES_SPECIAUX, **self.config.current_config["custom_entities"]}

    def previsualiser_conversion(self, contenu: str) -> None:
        """Crée une prévisualisation HTML du contenu converti"""
        html_preview = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Prévisualisation de la conversion</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 2em; }}
                .original, .converti {{ padding: 1em; border: 1px solid #ccc; margin: 1em 0; }}
                h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h2>Contenu Original</h2>
            <div class="original">{contenu}</div>
            <h2>Contenu Converti</h2>
            <div class="converti">{html.escape(contenu, quote=True)}</div>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
            f.write(html_preview)
            webbrowser.open('file://' + f.name)

    def convertir_caracteres_speciaux(self, input_path: str, output_path: str, mode_strict: bool = False) -> bool:
        """Version améliorée de la conversion avec prévisualisation et backup"""
        try:
            # Vérification et création du dossier de sortie
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Backup si activé
            if self.config.current_config["backup_files"]:
                backup_path = f"{output_path}.backup"
                if os.path.exists(output_path):
                    os.replace(output_path, backup_path)

            # Lecture et conversion
            with open(input_path, "r", encoding="utf-8") as file:
                contenu = file.read()

            # Prévisualisation si activée
            if self.config.current_config["preview_before_save"]:
                self.previsualiser_conversion(contenu)
                if not console.input("\nContinuer la conversion ? [y/N]: ").lower().startswith('y'):
                    return False

            # Conversion avec statistiques détaillées
            chars_avant = len(contenu)
            contenu_converti = html.escape(contenu, quote=True)
            
            for char, entity in self.caracteres_speciaux.items():
                contenu_converti = contenu_converti.replace(char, entity)
            
            # Métadonnées enrichies
            metadata = f"""
<!-- 
    Converti par Informaclique.fr
    Date de conversion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Fichier original: {os.path.basename(input_path)}
    Caractères convertis: {len(contenu_converti) - chars_avant}
    Version du convertisseur: 2.0
-->
"""
            contenu_converti += metadata

            # Écriture avec vérification
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(contenu_converti)

            self.stats["fichiers_traites"] += 1
            self.stats["caracteres_convertis"] += len(contenu_converti) - chars_avant
            logging.info(f"Conversion réussie pour {input_path}")
            return True

        except Exception as e:
            self.stats["erreurs"] += 1
            logging.error(f"Erreur lors de la conversion de {input_path}: {str(e)}")
            if mode_strict:
                raise
            return False

    def convertir_dossier(self, dossier_path: str, recursif: bool = False) -> None:
        """Conversion parallèle des fichiers d'un dossier"""
        fichiers_a_convertir = []
        
        for root, _, files in os.walk(dossier_path):
            if not recursif and root != dossier_path:
                continue

            for file in files:
                if file.lower().endswith(('.html', '.htm')):
                    input_path = os.path.join(root, file)
                    output_dir = os.path.join(self.config.current_config["default_output_dir"], 
                                            os.path.relpath(root, dossier_path))
                    output_path = os.path.join(output_dir, file.replace('.html', '_converti.html'))
                    fichiers_a_convertir.append((input_path, output_path))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Conversion des fichiers...", total=len(fichiers_a_convertir))
            
            with ThreadPoolExecutor(max_workers=self.config.current_config["max_workers"]) as executor:
                for input_path, output_path in fichiers_a_convertir:
                    executor.submit(self.convertir_caracteres_speciaux, input_path, output_path)
                    progress.advance(task)

    def afficher_statistiques(self) -> None:
        """Affichage amélioré des statistiques avec Rich"""
        table = Table(title="📊 Statistiques de conversion")
        
        table.add_column("Métrique", style="cyan")
        table.add_column("Valeur", justify="right", style="green")
        
        table.add_row("Fichiers traités", str(self.stats['fichiers_traites']))
        table.add_row("Caractères convertis", str(self.stats['caracteres_convertis']))
        table.add_row("Erreurs rencontrées", str(self.stats['erreurs']))
        
        console.print(Panel(table, title="Rapport de conversion", border_style="blue"))

    def configurer(self) -> None:
        """Interface de configuration"""
        console.print("\n[bold cyan]Configuration du convertisseur[/bold cyan]")
        
        self.config.current_config["mode_strict"] = console.input("Mode strict (True/False): ").lower() == "true"
        self.config.current_config["backup_files"] = console.input("Créer des backups (True/False): ").lower() == "true"
        self.config.current_config["preview_before_save"] = console.input("Prévisualiser avant sauvegarde (True/False): ").lower() == "true"
        
        try:
            max_workers = int(console.input("Nombre maximum de workers (1-8): "))
            self.config.current_config["max_workers"] = max(1, min(8, max_workers))
        except ValueError:
            console.print("[red]Valeur invalide, utilisation de la valeur par défaut (4)[/red]")
        
        self.config.sauvegarder_config()
        console.print("[green]Configuration sauvegardée avec succès![/green]")

def afficher_menu():
    """Interface utilisateur interactive améliorée"""
    convertisseur = ConvertisseurHTML()
    
    while True:
        console.print(Panel("""
🎯 Convertisseur d'entités HTML - Informaclique.fr

1. Convertir un fichier unique
2. Convertir tous les fichiers d'un dossier
3. Convertir récursivement (incluant sous-dossiers)
4. Afficher les statistiques
5. Configurer le convertisseur
6. Quitter
""", title="Menu Principal", border_style="cyan"))
        
        choix = console.input("\nVotre choix (1-6): ").strip()
        
        if choix == "1":
            input_path = console.input("\n📂 Chemin du fichier HTML à convertir: ").strip()
            if not os.path.exists(input_path):
                console.print("[red]❌ Le fichier spécifié n'existe pas.[/red]")
                continue
            output_path = input_path.replace(".html", "_converti.html")
            if convertisseur.convertir_caracteres_speciaux(input_path, output_path):
                console.print(f"[green]✅ Conversion réussie! Fichier sauvegardé: {output_path}[/green]")
        
        elif choix == "2" or choix == "3":
            dossier_path = console.input("\n📂 Chemin du dossier: ").strip()
            if not os.path.isdir(dossier_path):
                console.print("[red]❌ Le dossier spécifié n'existe pas.[/red]")
                continue
            convertisseur.convertir_dossier(dossier_path, recursif=(choix == "3"))
            console.print("[green]✅ Conversion terminée![/green]")
        
        elif choix == "4":
            convertisseur.afficher_statistiques()
        
        elif choix == "5":
            convertisseur.configurer()
        
        elif choix == "6":
            console.print("\n[cyan]👋 Merci d'avoir utilisé notre convertisseur![/cyan]")
            break
        
        else:
            console.print("[red]❌ Choix invalide. Veuillez réessayer.[/red]")

if __name__ == "__main__":
    try:
        afficher_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Programme interrompu par l'utilisateur[/yellow]")
    except Exception as e:
        logging.error(f"Erreur inattendue: {str(e)}")
        console.print(f"[red]Une erreur est survenue: {str(e)}[/red]")
