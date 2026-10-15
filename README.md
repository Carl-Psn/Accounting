# Accounting — equation comptable (NumWorks)

## Template slide 22 (statique)

[`template_slide22_periodic.py`](template_slide22_periodic.py) affiche le tableau **Rameau / méthode périodique** (slide 22) et les **six erreurs à éviter** (slide 23), **sans interaction**. Copier sur NumWorks → **Exécuter le script**. Pour un autre cas, dupliquer le fichier et modifier les lignes dans `TABLE` et la ligne `End`.

---

## Script interactif (`compta_equation.py`)

Script Python pour construire le **tableau d’équation comptable** (format slide 22 du *Midterm Review Study Guide 2026*), en **méthode périodique** uniquement, sur le modèle du cas **Rameau Co.**

## Fichier

- [`compta_equation.py`](compta_equation.py) — à copier dans l’application Python de la NumWorks

## Installation NumWorks

1. Aller sur [workshop.numworks.com](https://www.numworks.com/fr/python/) (ou l’éditeur Python depuis le site NumWorks).
2. Créer un nouveau script nommé **`compta`** (évitez **`test`**, nom ambigu).
3. Coller le contenu de `compta_equation.py`, transférer sur la calculatrice.

### Démarrer le menu (important)

Sur NumWorks, **Exécuter le script** ne lance pas `if __name__ == "__main__"` : la calculatrice fait `from compta import *`. Le script détecte NumWorks et appelle **`main()`** tout seul après l’import.

1. Liste des scripts → **`…`** à côté du nom → **Exécuter le script**.
2. Le menu « Equation comptable » doit s’afficher.

Si rien ne se passe (ancienne version du fichier) : à l’invite `>>>`, tapez **`main()`** ou **`demarrer()`** (touche **var** → choisir la fonction).

Si vous ouvrez seulement la **console Python** (shell) avec auto-import, le script se charge aussi ; avec la version à jour, le menu démarre après `from compta import *`.

## Utilisation à l’examen

1. Indiquer **periodic** sur votre copie (le script est déjà en mode périodique).
2. Pour chaque événement de l’énoncé, choisir le **numéro du template** (menu 1–14), puis entrer les montants demandés.
3. Après chaque écriture, un **résumé compact** s’affiche.
4. **Affichage sur NumWorks** : le tableau large (13 colonnes) peut bloquer la console. Le script affiche **une ligne par compte** (format court). Toutes les **4 écritures**, puis à la fin, tapez **`1`** puis **exe** quand vous voyez `1 puis exe = menu` (sinon la calculatrice semble « figée » en attendant).
5. **Sur NumWorks, utiliser uniquement des chiffres** dans « Choix » (les lettres C, D, etc. ne passent souvent pas dans `input()` sans mode alpha) :
   - **`91`** — tableau compact
   - **`92`** — grand tableau (slide 22)
   - **`93`** — soldes et vérification A = P + CP
   - **`94`** — démo Rameau
   - **`95`** — annuler la dernière écriture
   - **`96`** — réinitialiser
   - **`0`** — quitter
6. Amortissement linéaire auto : code **`15`** (plus besoin de `12a`).

## Templates (équivalents cas Rameau)

| Code | Événement |
|------|-----------|
| 1 | Apport des actionnaires (équipement + cash → capital) |
| 2 | Emprunt bancaire |
| 3 | Commande / promesse sans échange (**N/A**) |
| 4 | Acompte fournisseur (Avances / Caisse) |
| 5 | Réception marchandises — **achat en charge** (periodic) |
| 6 | Vente — **revenu seul** (periodic) |
| 7 | Loyer payé |
| 8 | Paiement fournisseur |
| 9 | Encaissement client |
| 10 | Personnel (salaires + charges sociales à payer) — 2 lignes |
| 11 | Intérêts payés |
| 12 | Amortissement (montant saisi) |
| 15 | Amortissement linéaire (coût ÷ durée) |
| 13 | Dividende déclaré |
| 14 | Inventaire de fin — **variation de stock** (periodic) |

## Vérification locale (PC)

```bash
python3 compta_equation.py test
```

Doit afficher **Test Rameau OK** avec actif **717** et résultat net **17**.

## Source

Basé sur `Midterm_Review_Study_Guide_2026.pdf` (Financial Accounting M1, octobre 2026).
