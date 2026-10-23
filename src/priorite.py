from typing import List

PRIORITE_MIN = 1
PRIORITE_MAX = 5
PRIORITE_BASE = 10
ALPHA_PAR_DEFAUT = 5


def calculer_score(colis, alpha: int = ALPHA_PAR_DEFAUT) -> int:
    p = min(max(colis.priorite, PRIORITE_MIN), PRIORITE_MAX)
    alpha = max(alpha, 0)
    return colis.valeur * (PRIORITE_BASE + alpha * (p - PRIORITE_MIN))


def calculer_scores(liste, alpha: int = ALPHA_PAR_DEFAUT) -> List[int]:
    return [calculer_score(c, alpha) for c in liste]
