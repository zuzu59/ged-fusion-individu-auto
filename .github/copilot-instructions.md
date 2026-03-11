---
applyTo: "**/*.py"
---

# Instructions Agent : Fusionneur GEDCOM via SQLite

## 1. Contexte du Projet
- **Objectif** : Utilitaire Python pour fusionner plusieurs fichiers GEDCOM (`individu_*.ged`) en un seul (`output.ged`), en éliminant les doublons d'individus et de familles tout en préservant l'intégrité des liens de parenté.
- **État actuel** : Projet vide. Première étape : créer `fusion.py` et l'architecture modulaire.
- **Workflow global** : Import successif (Extraction) -> Stockage SQLite (Transit/Merge) -> Export GEDCOM (Output).

## 2. Architecture Technique (Pipeline)
L'Agent doit implémenter le flux suivant :
1. **Extraction** : Parser chaque `individu_*.ged` source avec `python-gedcom`.
2. **Staging SQLite** : Insérer les données dans une base `sqlite3` (en mémoire ou fichier).
3. **Upsert Logique** : Identifier les doublons au moment de l'insertion pour ne pas polluer la base.
4. **Export** : Reconstruire l'objet `Gedcom` final depuis SQLite et l'enregistrer.

## 3. Logique de Dé-doublonnage (Priorité Haute)
L'Agent doit appliquer ces critères stricts pour identifier un individu déjà présent en base :
- **Critère A** : `(Nom exact) + (Prénom exact) + (Date de naissance)`.
- **Critère B (si date naissance NULL)** : `(Nom exact) + (Prénom exact) + (ID du Conjoint identique)`.
- **Normalisation** : Les comparaisons de texte (noms/prénoms) doivent être insensibles à la casse (`LOWER`).

## 4. Règles Métier & Intégrité
### Gestion des Individus
- **Mapping des IDs** : Créer une table de correspondance entre les XREFs originaux (`@I1@`, `@F1@`) et les IDs auto-incrémentés de SQLite.
- **Fusion de données** : En cas de doublon, transférer/fusionner les tags `NOTE` et `SOUR` vers l'entrée conservée.
- **Orphelins** : Un individu sans parents connus et non trouvé en base est marqué "Racine".

### Gestion des Familles & Unions
- **Identification Famille** : Une famille est unique par le couple `(ID_Mari + ID_Femme)`.
- **Unions Multiples** : Un individu peut appartenir à plusieurs familles (plusieurs mariages). Ne jamais fusionner deux familles si l'un des conjoints diffère.
- **Monoparentalité** : Accepter les familles avec un parent `NULL`. Une famille monoparentale est un doublon si elle a le même parent ET au moins un enfant commun avec une famille existante.
- **Enfants** : Un enfant ne doit être rattaché qu'une seule fois à une même famille (contrainte `UNIQUE` sur `id_enfant + id_famille`).

## 5. Schéma de Données SQLite (Recommandé)
- `individuals` : (id, nom, prenom, date_naiss, sexe, id_origine_gedcom)
- `families` : (id, id_mari, id_femme, date_mariage, lieu_mariage)
- `family_links` : (id_famille, id_individu, role) -- roles: 'HUSB', 'WIFE', 'CHIL'

## 6. Standards de Développement
- **Style** : Programmation orientée objet (classes pour `Individual`, `Family`, `DatabaseManager`).
- **Qualité** : Annotations de type obligatoires, Docstrings (format Google), gestion des erreurs via Exceptions.
- **Tests** : Utiliser `pytest`. Créer des tests unitaires pour chaque critère de matching.
- **Journalisation** : Logs détaillés de chaque fusion pour traçabilité (Audit Trail).

## 7. Commandes de Référence
- Installation : `pip install python-gedcom`
- Exécution : `python3 fusion.py <input1.ged> <input2.ged> ... <output.ged>`
- Validation : Utiliser `pytest` pour valider la non-régression.
