"""Génère le graphique des performances : python3 src/graphique.py

Relance les mesures de benchmark.py pour 100, 1 000, 10 000 et 100 000 colis,
puis trace une courbe par opération (échelles logarithmiques) avec matplotlib.
L'image est enregistrée dans captures/courbes.png.
"""

import os

import matplotlib
matplotlib.use("Agg")   # pas de fenêtre : on enregistre directement l'image
import matplotlib.pyplot as plt

from benchmark import TAILLES, CAPACITE_BENCH, NB_RECHERCHES, mesurer

COURBES = [
    ("rech. lin.", f"Recherche linéaire ({NB_RECHERCHES} rech.)", "#c0392b"),
    ("rech. dict", f"Recherche dict ({NB_RECHERCHES} rech.)", "#27ae60"),
    ("tri fusion", "Tri fusion", "#2c6fbb"),
    ("tri comptage", "Tri par comptage", "#16a085"),
    ("tri insertion", "Tri par insertion", "#8e44ad"),
    ("sac a dos DP", f"Sac à dos DP (W = {CAPACITE_BENCH})", "#d68910"),
]


def main() -> None:
    resultats = {}
    for n in TAILLES:
        print(f"Mesures pour {n} colis...", flush=True)
        resultats[n] = mesurer(n)

    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=200)
    for cle, libelle, couleur in COURBES:
        # le tri par insertion n'est pas mesuré pour les grandes tailles (valeur None)
        xs = [n for n in TAILLES if resultats[n][cle] is not None]
        ys = [resultats[n][cle] for n in xs]
        ax.plot(xs, ys, marker="o", label=libelle, color=couleur, linewidth=1.8)

    # Échelles logarithmiques : une pente de 1 correspond à O(n), une pente de 2 à O(n²)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Nombre de colis n")
    ax.set_ylabel("Temps (ms)")
    ax.set_title("Temps mesurés en fonction de n (échelles logarithmiques)", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7.5, loc="upper left", frameon=False)
    fig.tight_layout()

    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "captures")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.normpath(os.path.join(dossier, "courbes.png"))
    fig.savefig(chemin)
    print(f"Graphique enregistré : {chemin}")


if __name__ == "__main__":
    main()
