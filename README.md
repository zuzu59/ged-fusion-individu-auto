# ged-fusion-individu-auto
Petit script en python pour fusionner automatiquement des individus qui ont le Nom, Prénom et date de naissance les même

## Utilisation

```sh
python3 fusion.py input.ged output.ged
```

Le script produit un nouveau fichier GEDCOM où :

* les individus dupliqués (Nom/Prénom/Date de naissance identiques) ne
  figurent qu'une seule fois ;
* les familles redondantes (même mari, même épouse et mêmes enfants,
  après canonicisation des individus) sont supprimées.

Toutes les références aux identifiants supprimés sont remplacées par
celui de l'élément conservé, que ce soit dans les enregistrements
individuels ou familiaux, ce qui évite des « orphelins ».

