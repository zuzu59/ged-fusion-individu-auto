# Petit script en python pour fusionner des fichiers gedcom

📌 **État actuel** : le dépôt contient uniquement des exemples GEDCOM et
des consignes. Le code sera ajouté dans `fusion.py` et des modules
auxiliaires.

zf26037.1630, zf 260310.1428

## Problématiques du projet
J'ai un très grand arbre généalogique de 240'000 individus !

De cet arbre j'exporte plusieurs individus avec leurs ascendants et descendants dans des fichiers gedcom séparés:

individu_1.ged
individu_2.ged
individu_3.ged
...
individu_n.ged

Les fichiers gedcom ont donc des parties d'abres en commun !

Le but du projet est de réunir tous ces fichiers généalogiques gedcom, individu_1...n.ged, en un seul output.ged, sans les parties communes des arbres généalogiques tout en gardant les affiliations familiales des individus !



## Utilisation

Après avoir installé la dépendance `python-gedcom` et implémenté
le script `fusion.py`, exécutez :

```bash
python3 fusion.py individu_1.ged individu_2.ged ... output.ged
```

Pour lancer la suite de tests (une fois disponibles) :

```bash
pytest
```



## Validations du GEDCOM
Il faut utiliser le viewer Topola pour la vérification *visuelle* de la qualité du fichier GEDCOM:

https://pewu.github.io/topola-viewer/

Et *Ged-Inline* pour la vérification *syntaxique* de la qualité du fichier GEDCOM:

https://ged-inline.org/


