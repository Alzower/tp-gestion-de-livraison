# Gestion des livraisons — TP Algorithmique (Python)

Programme console qui gère une collection de colis (ajout, affichage, recherche, tris)
et prépare le chargement optimal d'un camion de capacité limitée.

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Graphique des performances](#graphique-des-performances)
- [Architecture du projet](#architecture-du-projet)
- [Choix algorithmiques](#choix-algorithmiques)
- [Dépannage](#dépannage)

## Prérequis

| Outil  | Version                         | Remarque                          |
| ------ | ------------------------------- | --------------------------------- |
| Python | **3.8 ou plus** (testé en 3.13) | Vérifier avec `python3 --version` |
| pip    | fourni avec Python              | Pour installer les dépendances    |
| Git    | optionnel                       | Pour cloner le dépôt              |

Le programme principal n'utilise que la bibliothèque standard.
La seule dépendance externe est **matplotlib** (>= 3.5), utilisée uniquement pour le graphique des performances.

## Installation

```bash
# 1. Récupérer le projet
git clone https://github.com/Alzower/tp-gestion-de-livraison.git
cd tp-gestion-de-livraison

# 2. Créer un environnement virtuel
python3 -m venv .venv

# 3. L'activer
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows (cmd / PowerShell)

# 4. Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
python3 src/main.py
```

Au démarrage, les 5 colis d'exemple de l'énoncé sont chargés. Menu :

| Option | Action                                                  |
| ------ | ------------------------------------------------------- |
| 1      | Afficher les colis                                      |
| 2      | Ajouter un colis                                        |
| 3      | Rechercher un colis (par identifiant)                   |
| 4      | Organiser les colis (tri par poids, valeur ou priorité) |
| 5      | Préparer un camion (valeur max, ou valeur + priorité)   |
| 6      | Afficher le chargement                                  |
| 7      | Afficher les statistiques                               |
| 8      | Générer des colis aléatoires                            |
| 9      | Mesurer les performances                                |
| 0      | Quitter                                                 |

## Graphique des performances

```bash
python3 src/graphique.py
```

Relance les mesures (100 à 100 000 colis) et enregistre `captures/courbes.png`.
Les mesures viennent de `benchmark.py` ; matplotlib sert uniquement à dessiner.

## Architecture du projet

```
tp-gestion-de-livraison/
├── src/
│   ├── main.py          point d'entrée
│   ├── menu.py          interface console (classe Application, actions du menu)
│   ├── colis.py         classe Colis + GestionnaireColis (liste + dictionnaire id -> colis), affichage
│   ├── tri.py           tri fusion, tri par comptage, tri par insertion (comparaison)
│   ├── priorite.py      score combinant valeur et priorité
│   ├── sac_a_dos.py     chargement : programmation dynamique, glouton, force brute
│   ├── benchmark.py     génération de données et mesures de temps
│   └── graphique.py     graphique des performances (captures/courbes.png)
├── captures/            captures d'écran et courbes du rapport
├── requirements.txt     dépendances (matplotlib)
├── Gestion des livraisons.pdf   énoncé du TP
├── rapport.pdf          rapport
└── README.md
```

### Dépendances entre modules

```
main ──► menu ──► colis
          │ ├───► tri
          │ ├───► priorite
          │ ├───► sac_a_dos ──► colis
          │ └───► benchmark ──► colis, tri, sac_a_dos
graphique ──► benchmark
```

## Choix algorithmiques

| Opération                 | Choix                                    | Temps           | Espace              |
| ------------------------- | ---------------------------------------- | --------------- | ------------------- |
| Ajout d'un colis          | Liste (tableau dynamique) + dictionnaire | O(1) amorti     | O(n)                |
| Recherche par identifiant | Dictionnaire (table de hachage)          | O(1) en moyenne | O(n)                |
| Tri par poids / valeur    | Tri fusion itératif (stable)             | O(n log n)      | O(n)                |
| Tri par priorité          | Tri par comptage (seaux)                 | O(n + k)        | O(n + k)            |
| Chargement du camion      | Sac à dos 0/1 en programmation dynamique | O(n × W)        | O(W) + n × W octets |

Le glouton et la force brute (`sac_a_dos.py`) et le tri par insertion (`tri.py`) servent de points de comparaison.

## Dépannage

- **`ModuleNotFoundError: matplotlib`** : l'environnement virtuel n'est pas activé ou `pip install -r requirements.txt` n'a pas été lancé. Seul `graphique.py` en a besoin.
- **`python3: command not found`** (Windows) : utiliser `python` ou `py` à la place.
- Lancer les commandes depuis la racine du projet.
