import csv
from datetime import datetime

from rich.console import Console
from rich.table import Table

console = Console()

SLOUPCE = ["číslo čipu", "zaměstnanec", "příchod", "odchod"]


def nacti_data(nazev_souboru):
    """
    Načte data z CSV souboru.
    :param nazev_souboru: Název souboru CSV
    :return: Seznam slovníků se záznamy docházky
    """
    data = []

    with open(nazev_souboru, "r", encoding="utf-8-sig", newline="") as soubor:
        reader = csv.DictReader(soubor, delimiter=";")

        for radek in reader:
            zaznam = {
                "číslo čipu": radek["číslo čipu"].strip(),
                "zaměstnanec": radek["zaměstnanec"].strip(),
                "příchod": datetime.strptime(
                    radek["příchod"].strip(), "%Y-%m-%d %H:%M"
                ),
                "odchod": datetime.strptime(
                    radek["odchod"].strip(), "%Y-%m-%d %H:%M"
                ),
            }

            data.append(zaznam)

    return data


def main():
    data = nacti_data("dochazka.csv")

    tabulka = Table(title="Evidence docházky")

    for sloupec in SLOUPCE:
        tabulka.add_column(sloupec)

    for zaznam in data:
        tabulka.add_row(
            zaznam["číslo čipu"],
            zaznam["zaměstnanec"],
            zaznam["příchod"].strftime("%Y-%m-%d %H:%M"),
            zaznam["odchod"].strftime("%Y-%m-%d %H:%M"),
        )

    console.print(tabulka)


if __name__ == "__main__":
    main()