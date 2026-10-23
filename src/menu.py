import time
from typing import Optional

from benchmark import generer_colis, lancer_benchmark
from colis import Colis, GestionnaireColis, afficher_entete, afficher_colis, afficher_tableau
from priorite import PRIORITE_MIN, PRIORITE_MAX, ALPHA_PAR_DEFAUT, calculer_scores
from sac_a_dos import (Chargement, afficher_chargement, sac_a_dos_dp,
                                 sac_a_dos_force_brute, sac_a_dos_glouton)
from tri import tri_comptage_priorite, tri_fusion

CAPACITE_MAX = 100_000
ALPHA_MAX = 50
FORCE_BRUTE_VERIF = 15   

COLIS_EXEMPLE = [
    Colis(101, 8, 20, 2, "Paris"),
    Colis(102, 3, 10, 5, "Lille"),
    Colis(103, 12, 40, 1, "Lyon"),
    Colis(104, 5, 25, 4, "Paris"),
    Colis(105, 2, 15, 3, "Lille"),
]


class Application:
    def __init__(self) -> None:
        self.gestionnaire = GestionnaireColis()
        self.chargement: Optional[Chargement] = None

    def charger_exemple(self) -> None:
        for c in COLIS_EXEMPLE:
            self.gestionnaire.ajouter(Colis(c.id, c.poids, c.valeur, c.priorite, c.destination))



def lire_entier(message: str, minimum: int, maximum: int) -> int:
    while True:
        saisie = input(message).strip()
        try:
            valeur = int(saisie)
            if minimum <= valeur <= maximum:
                return valeur
        except ValueError:
            pass
        print(f"  Saisie invalide : entrez un entier entre {minimum} et {maximum}.")


def lire_texte(message: str) -> str:
    while True:
        saisie = input(message).strip()
        if saisie:
            return saisie



def afficher_colis_menu(app: Application) -> None:
    print(f"\n--- Liste des colis ({len(app.gestionnaire)}) ---")
    afficher_tableau(app.gestionnaire.colis)


def ajouter_colis(app: Application) -> None:
    print("\n--- Ajouter un colis ---")
    identifiant = lire_entier("Identifiant : ", 1, 2**31 - 1)
    if app.gestionnaire.rechercher(identifiant) is not None:
        print(f"Un colis avec l'identifiant {identifiant} existe déjà.")
        return
    poids = lire_entier("Poids (kg) : ", 1, CAPACITE_MAX)
    valeur = lire_entier("Valeur : ", 0, 1_000_000)
    priorite = lire_entier("Priorité (1 = faible ... 5 = forte) : ", PRIORITE_MIN, PRIORITE_MAX)
    destination = lire_texte("Destination : ")
    app.gestionnaire.ajouter(Colis(identifiant, poids, valeur, priorite, destination))
    print(f"Colis {identifiant} ajouté.")


def rechercher_colis(app: Application) -> None:
    print("\n--- Rechercher un colis ---")
    identifiant = lire_entier("Identifiant : ", 1, 2**31 - 1)
    colis = app.gestionnaire.rechercher(identifiant)
    if colis is None:
        print(f"Aucun colis avec l'identifiant {identifiant}.")
    else:
        afficher_entete()
        afficher_colis(colis)


def organiser_colis(app: Application) -> None:
    print("\n--- Organiser les colis ---")
    if not app.gestionnaire.colis:
        print("Aucun colis.")
        return
    print("1. Par poids (croissant)       - tri fusion")
    print("2. Par valeur (décroissante)   - tri fusion")
    print("3. Par priorité (décroissante) - tri par comptage")
    choix = lire_entier("Choix : ", 1, 3)

    liste = app.gestionnaire.colis
    debut = time.perf_counter()
    if choix == 1:
        trie = tri_fusion(liste, lambda c: c.poids)
    elif choix == 2:
        trie = tri_fusion(liste, lambda c: c.valeur, decroissant=True)
    else:
        trie = tri_comptage_priorite(liste, PRIORITE_MIN, PRIORITE_MAX)
    duree = (time.perf_counter() - debut) * 1000

    afficher_tableau(trie)
    print(f"Tri de {len(trie)} colis en {duree:.3f} ms.")


def preparer_camion(app: Application) -> None:
    print("\n--- Préparer un camion ---")
    liste = app.gestionnaire.colis
    if not liste:
        print("Aucun colis à charger.")
        return
    capacite = lire_entier("Capacité du camion (kg) : ", 1, CAPACITE_MAX)
    print("1. Maximiser la valeur")
    print("2. Maximiser la valeur en favorisant la priorité")
    critere = lire_entier("Critère : ", 1, 2)
    if critere == 1:
        gains = [c.valeur for c in liste]
    else:
        alpha = lire_entier(f"Poids de la priorité alpha (0 = ignorée, {ALPHA_PAR_DEFAUT} = conseillé) : ",
                            0, ALPHA_MAX)
        gains = calculer_scores(liste, alpha)

    debut = time.perf_counter()
    try:
        chargement = sac_a_dos_dp(liste, gains, capacite)
    except MemoryError:
        print("Erreur : mémoire insuffisante (essayez une capacité plus petite).")
        return
    duree = (time.perf_counter() - debut) * 1000
    app.chargement = chargement

    print(f"\nChargement optimal (programmation dynamique, {duree:.3f} ms) :")
    afficher_chargement(chargement)

    glouton = sac_a_dos_glouton(liste, gains, capacite)
    print(f"\nComparaison glouton (ratio gain/poids) : score {glouton.score_total} "
          f"(valeur {glouton.valeur_totale}, {glouton.poids_total} kg)", end="")
    if glouton.score_total < chargement.score_total:
        print(f" -> moins bon de {chargement.score_total - glouton.score_total}")
    else:
        print(" -> identique ici")

    if len(liste) <= FORCE_BRUTE_VERIF:
        brute = sac_a_dos_force_brute(liste, gains, capacite)
        verdict = "optimal confirmé" if brute.score_total == chargement.score_total else "DIFFÉRENCE !"
        print(f"Vérification force brute : score {brute.score_total} -> {verdict}")


def afficher_chargement_menu(app: Application) -> None:
    print("\n--- Chargement du camion ---")
    if app.chargement is None:
        print("Aucun camion préparé.")
    else:
        afficher_chargement(app.chargement)


def afficher_statistiques(app: Application) -> None:
    print("\n--- Statistiques ---")
    liste = app.gestionnaire.colis
    n = len(liste)
    print(f"Nombre de colis : {n}")
    if n:
        poids = [c.poids for c in liste]
        valeur_totale = sum(c.valeur for c in liste)
        print(f"Poids total     : {sum(poids)} kg (moyenne {sum(poids) / n:.2f}, "
              f"min {min(poids)}, max {max(poids)})")
        print(f"Valeur totale   : {valeur_totale} (moyenne {valeur_totale / n:.2f})")
        print("Répartition par priorité :")
        compte = {p: 0 for p in range(PRIORITE_MIN, PRIORITE_MAX + 1)}
        for c in liste:
            if c.priorite in compte:
                compte[c.priorite] += 1
        for p in range(PRIORITE_MAX, PRIORITE_MIN - 1, -1):
            print(f"  priorité {p} : {compte[p]} colis")
    if app.chargement is not None:
        ch = app.chargement
        print(f"Dernier camion : {len(ch.colis)} colis, {ch.poids_total} / {ch.capacite} kg, "
              f"valeur {ch.valeur_totale}")


def generer_colis_menu(app: Application) -> None:
    print("\n--- Générer des colis aléatoires ---")
    n = lire_entier("Nombre de colis à générer : ", 1, 1_000_000)
    debut = time.perf_counter()
    generer_colis(app.gestionnaire, n)
    duree = (time.perf_counter() - debut) * 1000
    print(f"{n} colis générés en {duree:.3f} ms (total : {len(app.gestionnaire)}).")



ACTIONS = {
    1: afficher_colis_menu,
    2: ajouter_colis,
    3: rechercher_colis,
    4: organiser_colis,
    5: preparer_camion,
    6: afficher_chargement_menu,
    7: afficher_statistiques,
    8: generer_colis_menu,
    9: lambda app: lancer_benchmark(),
}


def menu_lancer(app: Application) -> None:
    while True:
        print("\n===== GESTION DES LIVRAISONS =====")
        print("1. Afficher les colis")
        print("2. Ajouter un colis")
        print("3. Rechercher un colis")
        print("4. Organiser les colis")
        print("5. Préparer un camion")
        print("6. Afficher le chargement")
        print("7. Afficher les statistiques")
        print("8. Générer des colis aléatoires")
        print("9. Mesurer les performances")
        print("0. Quitter")
        try:
            choix = lire_entier("Choix : ", 0, 9)
            if choix == 0:
                print("Au revoir.")
                return
            ACTIONS[choix](app)
            input("\nAppuyez sur Entrée pour continuer...")
        except (EOFError, KeyboardInterrupt):
            print()
            return
