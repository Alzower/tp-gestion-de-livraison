# Gestion des livraisons — TP Algorithmique (Python)

Programme console qui gère une collection de colis (ajout, affichage, recherche, tris)
et prépare le chargement optimal d'un camion de capacité limitée.

## Langage choisi : Python

- J'ai une préférence pour python pour sa lisibilité et sa simplicité. Je trouve que le C est plus verbeux et demande une gestion explicite de la mémoire.

## Lancer le programme

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

Nécessite Python 3.8 ou plus. Au démarrage, les 5 colis d'exemple de l'énoncé sont chargés.
Le menu permet aussi de générer des colis aléatoires (option 8) et de lancer les mesures (option 9).
Le programme lui-même n'utilise que la bibliothèque standard. La seule dépendance de `requirements.txt` est
**matplotlib**, utilisée uniquement pour dessiner le graphique des performances (voir ci-dessous).

## Générer le graphique des performances

```bash
python3 src/graphique.py
```

matplotlib est installé par `pip install -r requirements.txt` (étape ci-dessus).

Relance les mesures (100 à 100 000 colis) et enregistre `captures/courbes.png`.
matplotlib sert uniquement à dessiner : les mesures viennent de `benchmark.py`.

## Organisation du projet

```
src/
├── main.py         point d'entrée
├── colis.py        classe Colis + gestionnaire (liste + dictionnaire id -> colis)
├── tri.py          tri fusion, tri par comptage, tri par insertion (comparaison)
├── priorite.py     score combinant valeur et priorité
├── sac_a_dos.py    chargement : programmation dynamique, glouton, force brute
├── menu.py         interface console
├── benchmark.py    génération de données et mesures de temps
└── graphique.py    graphique des performances (captures/courbes.png)
requirements.txt   dépendances (matplotlib)
README.md
rapport.pdf
```

## Choix algorithmiques principaux

| Opération                 | Choix                                    | Temps           | Espace              |
| ------------------------- | ---------------------------------------- | --------------- | ------------------- |
| Ajout d'un colis          | Liste (tableau dynamique) + dictionnaire | O(1) amorti     | O(n)                |
| Recherche par identifiant | Dictionnaire (table de hachage)          | O(1) en moyenne | O(n)                |
| Tri par poids / valeur    | Tri fusion itératif (stable)             | O(n log n)      | O(n)                |
| Tri par priorité          | Tri par comptage (seaux)                 | O(n + k)        | O(n + k)            |
| Chargement du camion      | Sac à dos 0/1 en programmation dynamique | O(n × W)        | O(W) + n × W octets |
# tp-gestion-de-livraison
