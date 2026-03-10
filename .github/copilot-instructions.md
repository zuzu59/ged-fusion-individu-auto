---
applyTo: "**/*.py"
---
# Projet

Petit utilitaire en Python pour fusionner des fichiers GEDCOM
(extraits d'arbres généalogiques). Le script principal est
`fusion.py`, qui lit un `.ged`, dédoublonne individus et familles
et produit un GEDCOM nettoyé en sortie.

> ⚠️ **État actuel** : pour l'instant la base du dépôt ne contient que
quelques exemples `individu_*.ged` et ces instructions ; le code
Python n'a pas encore été écrit. Une des premières tâches est de
créer `fusion.py` et les modules associés, puis de définir des tests
pytest dans `tests/`.


# Architecture

Le cœur de l'application analysera plusieurs fichiers GEDCOM d'entrée,
sauvegardera les informations dans une base SQLite pour détecter et
éliminer les doublons, puis écrira un unique fichier de sortie
contenant l'arbre fusionné. La bibliothèque `python-gedcom` est
utilisée pour l'analyse/écriture, et le code doit être organisé en
modules/classements clairs afin de faciliter les tests et l'évolution.

# Organisation du dépôt

- `individu_*.ged` : exemples de fichiers GEDCOM d'entrée fournis pour
  le développement et les tests.
- `fusion.py` : script principal (sera ajouté lorsque le code sera
  implémenté).
- `tests/` : répertoire destiné aux tests `pytest`.
- `.github/` : contient cette instruction ainsi que les autres
  documents de configuration.

# Installation & exécution

- Ce projet cible Python 3.
- Installez la dépendance GEDCOM nécessaire :
  ```bash
  pip install python-gedcom
  ```
- Une fois le code en place, lancer les tests :
  ```bash
  pytest
  ```
- Exemple d'utilisation :
  ```bash
  python3 fusion.py input.ged output.ged
  ```
- Les fichiers GEDCOM en entrée peuvent être validés :
  - visuellement avec Topola : https://pewu.github.io/topola-viewer/
  - syntaxiquement avec Ged‑Inline : https://ged-inline.org/


# Style & conventions

- Utiliser la lib *pip install python-gedcom* pour manipuler le gedcom
- Utiliser la db sqlite pour la gestion des individus et recherche de parties communes de l'arbre généalogique
- Utiliser des classes pour représenter les individus et les familles
- Utiliser des fonctions pour les opérations sur les individus et les familles
- Utiliser des commentaires pour expliquer le code
- Utiliser des noms de variables et de fonctions explicites
- Utiliser des tests unitaires pour vérifier le bon fonctionnement du code
- Utiliser un linter pour vérifier la qualité du code
- Utiliser un formatteur pour uniformiser le code 
- Utiliser des exceptions pour gérer les erreurs
- Utiliser des docstrings pour documenter les fonctions et les classes
- Utiliser des annotations de type pour améliorer la lisibilité du code
- Utiliser des modules pour organiser le code
- Utiliser des packages pour organiser les modules

# Tests

- Préférer `pytest` et stocker les tests dans un dossier `tests/`.
- Les cas de test doivent couvrir l'analyse, la fusion et la validation
du GEDCOM.

# Notes supplémentaires

- Le projet n'a pas de système de build particulier ; il suffit de lancer
  le script.
- Le README contient des informations de base sur l'usage et la
  validation des GEDCOM.

