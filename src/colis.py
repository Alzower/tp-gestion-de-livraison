from dataclasses import dataclass
from typing import Dict, List, Optional

AFFICHAGE_MAX = 50


@dataclass
class Colis:
    id: int
    poids: int        
    valeur: int
    priorite: int   
    destination: str


class GestionnaireColis:
    def __init__(self) -> None:
        self.colis: List[Colis] = []
        self.index: Dict[int, Colis] = {}

    def __len__(self) -> int:
        return len(self.colis)

    def ajouter(self, colis: Colis) -> bool:
        if colis.id in self.index:
            return False
        self.colis.append(colis)
        self.index[colis.id] = colis
        return True

    def rechercher(self, identifiant: int) -> Optional[Colis]:
        return self.index.get(identifiant)

    def rechercher_lineaire(self, identifiant: int) -> Optional[Colis]:
        for colis in self.colis:
            if colis.id == identifiant:
                return colis
        return None


def afficher_entete() -> None:
    print(f"{'ID':<8} {'Poids':<8} {'Valeur':<8} {'Priorité':<9} Destination")
    print("-------- -------- -------- --------- --------------------")


def afficher_colis(colis: Colis) -> None:
    print(f"{colis.id:<8} {colis.poids:<8} {colis.valeur:<8} {colis.priorite:<9} {colis.destination}")


def afficher_tableau(liste: List[Colis], limite: Optional[int] = AFFICHAGE_MAX) -> None:
    if not liste:
        print("Aucun colis.")
        return
    a_afficher = liste if limite is None else liste[:limite]
    afficher_entete()
    for colis in a_afficher:
        afficher_colis(colis)
    if len(liste) > len(a_afficher):
        print(f"... et {len(liste) - len(a_afficher)} autres colis "
              f"(affichage limité aux {len(a_afficher)} premiers).")
