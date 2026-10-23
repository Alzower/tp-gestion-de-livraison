from typing import Callable, List, TypeVar

T = TypeVar("T")


def tri_fusion(elements: List[T], cle: Callable[[T], float], decroissant: bool = False) -> List[T]:
    signe = -1 if decroissant else 1
    a = [(signe * cle(e), e) for e in elements]
    n = len(a)
    if n < 2:
        return [e for _, e in a]
    b = [None] * n

    largeur = 1
    while largeur < n:
        for debut in range(0, n, 2 * largeur):
            milieu = min(debut + largeur, n)
            fin = min(debut + 2 * largeur, n)
            i, j, k = debut, milieu, debut
            while i < milieu and j < fin:
                if a[j][0] < a[i][0]:
                    b[k] = a[j]
                    j += 1
                else:
                    b[k] = a[i]
                    i += 1
                k += 1
            if i < milieu:
                b[k:fin] = a[i:milieu]
            else:
                b[k:fin] = a[j:fin]
        a, b = b, a
        largeur *= 2

    return [e for _, e in a]


def tri_comptage_priorite(elements: List[T], prio_min: int, prio_max: int) -> List[T]:
    k = prio_max - prio_min + 1
    seaux: List[List[T]] = [[] for _ in range(k)]
    for e in elements:
        p = min(max(e.priorite, prio_min), prio_max)
        seaux[prio_max - p].append(e)
    return [e for seau in seaux for e in seau]


def tri_insertion(elements: List[T], cle: Callable[[T], float], decroissant: bool = False) -> List[T]:
    signe = -1 if decroissant else 1
    a = [(signe * cle(e), e) for e in elements]
    for i in range(1, len(a)):
        courant = a[i]
        j = i
        while j > 0 and a[j - 1][0] > courant[0]:
            a[j] = a[j - 1]
            j -= 1
        a[j] = courant
    return [e for _, e in a]
