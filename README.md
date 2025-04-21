# 🚀 Convertisseur d'Entités HTML Pro

Un outil Python professionnel et moderne pour convertir automatiquement les caractères spéciaux en entités HTML dans vos fichiers. Idéal pour garantir la compatibilité maximale de vos pages web sur tous les navigateurs et environnements.

## ✨ Caractéristiques

### 🛠️ Fonctionnalités Principales
- **Conversion Intelligente** : Transformation automatique des caractères spéciaux en entités HTML
- **Interface Moderne** : Interface utilisateur colorée et intuitive avec la bibliothèque `rich`
- **Prévisualisation** : Aperçu des conversions dans votre navigateur avant validation
- **Traitement par Lots** : Conversion de dossiers entiers avec support récursif
- **Multi-threading** : Conversion parallèle pour des performances optimales
- **Sauvegarde Automatique** : Backup automatique des fichiers avant modification

### 🎯 Caractères Supportés
- **Lettres Accentuées** : é, è, à, â, ê, î, ô, û, ë, ï, ü, ÿ, ç...
- **Symboles Courants** : €, £, ¥, ©, ®, ™, °, ±...
- **Fractions et Exposants** : ¼, ½, ¾, ², ³, ¹...
- **Ponctuation Typographique** : «, », ‹, ›, —, –, …
- **Symboles Mathématiques** : ∑, ∏, ∂, ∞, ∫, ≈, ≠, ≤, ≥...

### ⚙️ Configuration Avancée
- Mode strict pour la gestion des erreurs
- Création automatique de backups
- Prévisualisation configurable
- Nombre de workers personnalisable
- Dossier de sortie configurable
- Support d'entités personnalisées

## 📋 Prérequis

- Python 3.7 ou supérieur
- Dépendances listées dans `requirements.txt`

## 🔧 Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/HTML-Entity-Converter-Pro.git
   cd HTML-Entity-Converter-Pro
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Utilisation

### Démarrage Rapide
1. Lancer le script :
   ```bash
   python correctcode.py
   ```
2. Choisir une option dans le menu principal
3. Suivre les instructions à l'écran

### Options du Menu
1. **Convertir un fichier unique**
   - Conversion d'un seul fichier HTML avec prévisualisation
   - Backup automatique du fichier original

2. **Convertir un dossier**
   - Conversion de tous les fichiers HTML d'un dossier
   - Conservation de la structure des dossiers

3. **Conversion récursive**
   - Traitement des sous-dossiers
   - Conversion parallèle pour de meilleures performances

4. **Statistiques**
   - Nombre de fichiers traités
   - Nombre de caractères convertis
   - Erreurs rencontrées

5. **Configuration**
   - Mode strict
   - Gestion des backups
   - Prévisualisation
   - Performances (nombre de workers)

## 📊 Exemples

### Exemple de Conversion
Avant :
```html
<p>Voici un texte avec des caractères spéciaux : été, œuf, 23°C, copyright ©</p>
```

Après :
```html
<p>Voici un texte avec des caract&egrave;res sp&eacute;ciaux : &eacute;t&eacute;, &oelig;uf, 23&deg;C, copyright &copy;</p>
```

## 📝 Logs et Suivi

- Les logs sont automatiquement sauvegardés dans `conversion_log.txt`
- Rotation automatique des logs (max 5 fichiers de 1MB)
- Statistiques détaillées disponibles dans l'interface

## ⚠️ Gestion des Erreurs

- Validation des fichiers d'entrée
- Mode strict optionnel
- Messages d'erreur explicites et colorés
- Backup automatique des fichiers

## 🔄 Configuration

Le fichier `converter_config.json` permet de personnaliser :
- Le mode de fonctionnement
- Les options de sauvegarde
- Les préférences d'interface
- Les performances

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 🙏 Remerciements

- Développé par Informaclique.fr
- Utilise la bibliothèque `rich` pour l'interface
- Inspiré par les besoins de la communauté web francophone

## 📞 Support

- Créez une issue sur GitHub pour les bugs
- Consultez la documentation pour plus d'informations
- Contactez-nous sur Informaclique.fr pour le support
