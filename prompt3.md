Ecrit un script en python 3, fusion.py, qui fusionne les doublons d'individus ayant exactement le même nom, prénom et date de naissance du fichier input.ged

Dans une première passe:

* La fusion ne doit pas se faire de manière séquentielle au moment de la lecture du fichier gedcom mais seulement après analyse car il y a des risques de récursivité !

* Le script donc analyse et cherche en premier les fusions d'individus possibles pour les mettre dans une table

* Puis après seulement fusionne les individus toujours dans une table en maintient les liaisons fraternelles : toutes les références (FAMC, FAMS, etc.) sont réécrites.


Dans une deuxième passe:

* Fait la même chose sur le résultat de la fusion des individus pour trouver les doublons des familles : les enregistrements FAM avec le même mari, la même épouse et les mêmes enfants (après canonisation des individus) ne sont conservés qu’une seule fois. Et ceci avec le résultat toujours dans une table


Dans une troisième passe:

* Le script refait la passe un et deux autant de fois que nécéssaire afin de bien vérifier qu'il n'y a plus de doublons d'individus ni de familles et que surtout les liaisons fraternelles par comparaison au fichier input.ged soient maintenues.


Et finalement:

* Et seulement quand tout est bon on sauvegarde le résultat dans le fichier output.ged
