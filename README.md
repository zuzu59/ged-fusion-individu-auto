# ged-fusion-individu-auto
Petit script en python pour fusionner automatiquement des individus qui ont le Nom, Prénom et date de naissance les même

## Utilisation

```sh
python3 fusion.py input.ged output.ged
```

Le script produit un nouveau fichier GEDCOM où les individus dupliqués
(Nom/Prénom/Date de naissance identiques) ne figurent qu'une seule fois.
Il remplace également dans les enregistrements familiaux toutes les
références aux identifiants supprimés par celui de l'individu conservé,
ce qui évite des « orphelins » comme Jean Louis Bertrand ZUFFEREY.

