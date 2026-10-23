import random
import time
from typing import Callable

from colis import Colis, GestionnaireColis
from priorite import PRIORITE_MIN, PRIORITE_MAX
from sac_a_dos import sac_a_dos_dp
from tri import tri_fusion, tri_comptage_priorite, tri_insertion

TAILLES = [100, 1_000, 10_000, 100_000]
NB_RECHERCHES = 1_000
CAPACITE_BENCH = 200        
LIMITE_INSERTION = 10_000    
VILLES = ["Paris", "Lille", "Lyon", "Marseille", "Bordeaux", "Nantes", "Toulouse", "Strasbourg"]


def generer_colis(gestionnaire: GestionnaireColis, n: int, graine=None) -> None:
    alea = random.Random(graine)
    prochain_id = 1
    for _ in range(n):
        while prochain_id in gestionnaire.index:
            prochain_id += 1
        gestionnaire.ajouter(Colis(
            id=prochain_id,
            poids=alea.randint(1, 50),
            valeur=alea.randint(1, 100),
            priorite=alea.randint(PRIORITE_MIN, PRIORITE_MAX),
            destination=alea.choice(VILLES),
        ))
        prochain_id += 1


def chronometrer(fonction: Callable[[], object]) -> float:
    debut = time.perf_counter()
    fonction()
    return (time.perf_counter() - debut) * 1000


def mesurer(n: int) -> dict:
    g = GestionnaireColis()
    generer_colis(g, n, graine=42)
    alea = random.Random(0)
    ids = [alea.choice(g.colis).id for _ in range(NB_RECHERCHES)]
    gains = [c.valeur for c in g.colis]

    def recherches_lineaires():
        for i in ids:
            g.rechercher_lineaire(i)

    def recherches_hachage():
        for i in ids:
            g.rechercher(i)

    return {
        "rech. lin.": chronometrer(recherches_lineaires),
        "rech. dict": chronometrer(recherches_hachage),
        "tri fusion": chronometrer(lambda: tri_fusion(g.colis, lambda c: c.poids)),
        "sorted()": chronometrer(lambda: sorted(g.colis, key=lambda c: c.poids)),
        "tri comptage": chronometrer(lambda: tri_comptage_priorite(g.colis, PRIORITE_MIN, PRIORITE_MAX)),
        "tri insertion": (chronometrer(lambda: tri_insertion(g.colis, lambda c: c.poids))
                          if n <= LIMITE_INSERTION else None),
        "sac a dos DP": chronometrer(lambda: sac_a_dos_dp(g.colis, gains, CAPACITE_BENCH)),
    }


def lancer_benchmark() -> None:
    print("\n--- Mesures de performances (temps en ms) ---")
    print(f"Recherches : {NB_RECHERCHES} recherches d'identifiants existants.")
    print(f"Sac à dos  : capacité {CAPACITE_BENCH} kg. "
          f"Tri par insertion ignoré au-delà de {LIMITE_INSERTION} colis.")
    print("sorted() = tri natif de Python (Timsort), donné pour comparaison.\n")

    colonnes = ["rech. lin.", "rech. dict", "tri fusion", "sorted()",
                "tri comptage", "tri insertion", "sac a dos DP"]
    print(f"{'n':>8} | " + " | ".join(f"{c:>13}" for c in colonnes) + " |")
    print("-" * 9 + "+" + ("-" * 15 + "+") * len(colonnes))
    for n in TAILLES:
        resultats = mesurer(n)
        cellules = [f"{resultats[c]:>13.3f}" if resultats[c] is not None else f"{'-':>13}"
                    for c in colonnes]
        print(f"{n:>8} | " + " | ".join(cellules) + " |", flush=True)
