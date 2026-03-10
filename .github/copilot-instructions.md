---
applyTo: "**/*.py"
---
# Projet

Petit utilitaire en Python pour fusionner des fichiers GEDCOM
(extraits d'arbres généalogiques). Le script principal est
`fusion.py`, qui lit un `.ged`, dédoublonne individus et familles
et produit un GEDCOM nettoyé en sortie.

# Installation & exécution

- Ce projet cible Python 3.
- Installez la dépendance GEDCOM nécessaire :
  ```bash
  pip install python-gedcom
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

