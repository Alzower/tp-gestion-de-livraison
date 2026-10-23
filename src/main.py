from menu import Application, menu_lancer


def main() -> None:
    app = Application()
    app.charger_exemple()
    print("Les 5 colis d'exemple de l'énoncé ont été chargés.")
    menu_lancer(app)


if __name__ == "__main__":
    main()
