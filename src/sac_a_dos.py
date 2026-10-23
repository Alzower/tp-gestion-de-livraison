
from dataclasses import dataclass, field
from operator import gt
from typing import List

from colis import Colis, afficher_entete, afficher_colis
from tri import tri_fusion

FORCE_BRUTE_N_MAX = 20
MEMOIRE_MAX = 300_000_000  

@dataclass
class Chargement:
    capacite: int
    colis: List[Colis] = field(default_factory=list)
    poids_total: int = 0
    valeur_totale: int = 0
    score_total: int = 0

    def ajouter(self, colis: Colis, gain: int) -> None:
        self.colis.append(colis)
        self.poids_total += colis.poids
        self.valeur_totale += colis.valeur
        self.score_total += gain


def sac_a_dos_dp(liste: List[Colis], gains: List[int], capacite: int) -> Chargement:
    W = capacite
    resultat = Chargement(capacite=W)
    if W <= 0 or not liste:
        return resultat

    utiles = [i for i, c in enumerate(liste) if 0 < c.poids <= W and gains[i] > 0]
    if len(utiles) * (W + 1) > MEMOIRE_MAX:
        raise MemoryError("table de programmation dynamique trop grande")

    meilleur = [0] * (W + 1)
    choix = []

    for i in utiles:
        p = liste[i].poids
        g = gains[i]
        candidats = [v + g for v in meilleur[:W + 1 - p]]
        anciens = meilleur[p:]
        pris = bytes(map(gt, candidats, anciens))
        meilleur = meilleur[:p] + list(map(max, candidats, anciens))
        choix.append((i, bytes(p) + pris))

    w = W
    selection = []
    for i, ligne in reversed(choix):
        if ligne[w]:
            selection.append(i)
            w -= liste[i].poids
    for i in reversed(selection):
        resultat.ajouter(liste[i], gains[i])
    return resultat


def sac_a_dos_glouton(liste: List[Colis], gains: List[int], capacite: int) -> Chargement:
    resultat = Chargement(capacite=capacite)
    candidats = [i for i, c in enumerate(liste) if 0 < c.poids <= capacite and gains[i] > 0]
    ordre = tri_fusion(candidats, lambda i: gains[i] / liste[i].poids, decroissant=True)
    restant = capacite
    for i in ordre:
        if liste[i].poids <= restant:
            resultat.ajouter(liste[i], gains[i])
            restant -= liste[i].poids
    return resultat


def sac_a_dos_force_brute(liste: List[Colis], gains: List[int], capacite: int) -> Chargement:
    n = len(liste)
    if n > FORCE_BRUTE_N_MAX:
        raise ValueError(f"force brute limitée à {FORCE_BRUTE_N_MAX} colis")
    meilleur_masque, meilleur_gain = 0, 0
    for masque in range(1 << n):
        poids = gain = 0
        for i in range(n):
            if masque >> i & 1:
                poids += liste[i].poids
                if poids > capacite:
                    break
                gain += gains[i]
        if poids <= capacite and gain > meilleur_gain:
            meilleur_gain, meilleur_masque = gain, masque
    resultat = Chargement(capacite=capacite)
    for i in range(n):
        if meilleur_masque >> i & 1:
            resultat.ajouter(liste[i], gains[i])
    return resultat


def afficher_chargement(chargement: Chargement) -> None:
    if not chargement.colis:
        print("Aucun colis chargé.")
    else:
        afficher_entete()
        for c in chargement.colis:
            afficher_colis(c)
    remplissage = 100 * chargement.poids_total / chargement.capacite if chargement.capacite else 0
    print(f"\nColis chargés  : {len(chargement.colis)}")
    print(f"Poids total    : {chargement.poids_total} / {chargement.capacite} kg ({remplissage:.1f} %)")
    print(f"Valeur totale  : {chargement.valeur_totale}")
    print(f"Score optimisé : {chargement.score_total}")
