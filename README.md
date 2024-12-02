HTML-Entity-Converter
Un outil Python interactif pour convertir automatiquement les caractères spéciaux en entités HTML dans un fichier HTML. Ce script est conçu pour résoudre les problèmes d'encodage et garantir la compatibilité des fichiers HTML sur tous les navigateurs et environnements.

🎯 Fonctionnalités

Conversion automatique : Transforme les caractères spéciaux (ex. é, è, à, ', ") en entités HTML (&eacute;, &egrave;, &agrave;, &rsquo;, &quot;).
Interface simple : Demande directement le chemin du fichier à convertir via une interface utilisateur en ligne de commande.
Fichier de sortie généré automatiquement : Sauvegarde le fichier converti avec un suffixe _converti.html dans le même dossier.
Mention personnalisée : Ajoute automatiquement une mention au bas du fichier HTML (<!-- Converti par Informaclique.fr -->) pour promouvoir la marque.
Vérification des erreurs : Vérifie que le fichier d'entrée existe et affiche des messages clairs en cas de problème.

🛠️ Prérequis

Python 3.6 ou version ultérieure
Aucune dépendance externe requise (le script utilise uniquement des bibliothèques standard de Python).

🚀 Installation

Clone ce dépôt sur ton ordinateur :

bash
Copier le code
git clone https://github.com/ton-utilisateur/HTML-Entity-Converter.git
Accède au dossier du projet :

bash
Copier le code
cd HTML-Entity-Converter

📖 Utilisation
Lancer le script :

bash

python html_entity_converter.py
Fournir le chemin complet du fichier HTML à convertir lorsque le script le demande.

Le script génère un nouveau fichier contenant les entités HTML converties et ajoute une mention à Informaclique.fr.

💡 Exemple
Fichier d'entrée (avant conversion) :
html
<p>Voici une phrase avec des caractères spéciaux : é, è, à, ', ".</p>
Fichier de sortie (après conversion) :
html

<p>Voici une phrase avec des caract&egrave;res sp&eacute;ciaux : &eacute;, &egrave;, &agrave;, &rsquo;, &quot;.</p>
<!-- Converti par Informaclique.fr -->
🤝 Contribuer
Les contributions sont les bienvenues ! Si tu souhaites améliorer ce projet ou ajouter des fonctionnalités, voici comment procéder :

Fork ce dépôt.
Crée une branche pour tes modifications : git checkout -b nouvelle-fonctionnalite.
Commit tes changements : git commit -m "Ajout d'une nouvelle fonctionnalité".
Push la branche : git push origin nouvelle-fonctionnalite.
Ouvre une Pull Request.
