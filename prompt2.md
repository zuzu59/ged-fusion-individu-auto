Le fichier fusion.py est un petit utilitaire Python 3 qui lit un fichier GEDCOM, fusionne les doublons d’individus puis de familles, valide le résultat et écrit le GEDCOM nettoyé dans un second fichier.

🛠 Fonctionnalités implémentées
1. Parsing GEDCOM
   * Sépare le flux en enregistrements (INDI, FAM, etc.).
   * Prend en compte les niveaux (0, 1, 2, …) pour une validation basique.

1. Première passe – individus
   * Regroupe les individus possédant exactement le même nom, prénom et date de naissance.
   * Choisit le premier individu rencontré comme « canonique ».
   * Réécrit toutes les références (FAMC, FAMS, …) pour pointer vers l’ID canonique.
   * Conserve les lignes supplémentaires des doublons dans l’individu retenu.

1. Deuxième passe – familles
   * Détecte les familles identiques (même mari, même épouse, mêmes enfants) après canonicalisation des individus.
   * Fusionne ces familles de manière itérative jusqu’à ce qu’il ne reste plus de duplicata.
   * Met à jour les références familiales (FAMC, FAMS) dans les fiches d’individus.

1. Validation GEDCOM
   * Vérifie l’unicité des ID.
   *Contrôle la séquence des niveaux.
   * Souhaite la présence de toutes les références (@I…@, @F…@).

   Les erreurs sont envoyées sur stderr mais n’empêchent pas l’écriture du fichier de sortie.

1. Écriture
   * Reconstruit le fichier en respectant l’ordre d’apparition original (première occurrence d’un individu ou d’une famille).
   * Tous les enregistrements restants sont écrits dans output.ged.

Exemple d’utilisation
```
python3 fusion.py input.ged output.ged
```

* ```input.ged``` : fichier source
* ```output.ged``` : fichier nettoyé

Les éventuelles erreurs de validation sont affichées sur la sortie d’erreur.