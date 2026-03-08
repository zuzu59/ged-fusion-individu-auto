Ecrit un petit script, fusion.py, en python 3 qui:

Dans une première passe:

* Depuis le fichier, input.ged, fusionne les individus ayant exactement le même nom, prénom et date de naissance.

* Maintient les liaisons fraternelles : toutes les références (FAMC, FAMS, etc.) sont réécrites.

Dans une deuxième passe:

* Supprime aussi les doublons de familles : les enregistrements FAM avec le même mari, la même épouse et les mêmes enfants (après canonisation des individus) ne sont conservés qu’une seule fois. Et fais-le autant de fois que nécéssaire !

* Elimine les 'duplicate occurrence of label'

* Sauvegarde le résultat dans le fichier output.ged
