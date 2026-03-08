Ecrit un petit script, fusion.py, en python 3 qui:

* Fusionne les individus ayant exactement le même Nom, Prénom et date de naissance.

* Maintient les liaisons fraternelles : toutes les références (FAMC, FAMS, etc.) sont réécrites.

* Supprime aussi les doublons de familles : les enregistrements FAM avec le même mari, la même épouse et les mêmes enfants (après canonisation des individus) ne sont conservés qu’une seule fois.

* Effectue une validation GEDCOM exhaustive

* Sauvegarde le résultat dans le fichier output.ged
