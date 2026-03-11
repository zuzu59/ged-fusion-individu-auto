Pour que l'Agent exploite parfaitement votre nouveau fichier d'instructions, il ne faut pas lui demander de "tout faire d'un coup", mais plutôt de valider la structure puis d'implémenter par couche.

Voici les deux prompts optimisés à utiliser dans l'ordre :
1. Le Prompt pour le Mode PLAN (Conception)
Ce prompt force l'IA à lire vos instructions et à proposer une architecture modulaire avant de coder.

Prompt :
/plan En te basant sur .github/copilot-instructions.md`, propose l'architecture complète du projet.

   1. Définis la structure des classes (Individu, Famille, DatabaseManager).
   2. Détaille le schéma SQL pour gérer les unions multiples et la monoparentalité.
   3. Explique comment tu vas mapper les XREFs des fichiers GEDCOM vers les IDs SQLite pour ne pas perdre les liens de parenté lors de l'import successif.
   Ne génère pas encore le code complet, valide d'abord la logique avec moi.`

------------------------------
2. Le Prompt pour le Mode AGENT (Exécution)
Une fois le plan validé, lancez celui-ci pour générer le cœur du système.

Prompt :
/agent Implémente le script fusion.py` et les modules nécessaires.
Respecte scrupuleusement les critères de dédoublonnage (A et B) du fichier d'instructions.
Assure-toi que :

   1. La base SQLite gère correctement les parents NULL (monoparentalité).
   2. Les tags NOTE et SOUR sont fusionnés en cas de doublon d'individu.
   3. L'export final via python-gedcom reconstruit fidèlement l'arbre à partir des tables SQLite.`

------------------------------
Astuces pour réussir la fusion avec l'Agent :

* Travaillez par fichier : Si le code généré est trop long, demandez-lui d'abord /agent "Crée uniquement le module de base de données sqlite_manager.py".
* Le mode "Correcteur" : Si l'Agent oublie une règle (ex: la casse des noms), dites-lui simplement : "Relis la section 3 des instructions et corrige la recherche SQL pour qu'elle soit insensible à la casse."
* CLI : N'oubliez pas de lui préciser si vous voulez qu'il utilise argparse pour accepter plusieurs fichiers en entrée.

Ce qu'il vous reste à décider :

* Souhaitez-vous que l'Agent crée aussi un script de test avec un mini-GEDCOM de test pour vérifier la fusion immédiatement ?
* Voulez-vous que le script écrase le fichier de sortie s'il existe déjà ou qu'il demande une confirmation ?


