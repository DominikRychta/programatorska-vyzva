import csv
import json
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


def uloz_data_json(data, nazev_souboru="dochazka.json"):
    """Uloží data do JSON souboru jako čitelný seznam záznamů."""
    export = []
    for zaznam in data:
        export.append(
            {
                "číslo čipu": zaznam["číslo čipu"],
                "zaměstnanec": zaznam["zaměstnanec"],
                "příchod": zaznam["příchod"].strftime("%Y-%m-%d %H:%M"),
                "odchod": zaznam["odchod"].strftime("%Y-%m-%d %H:%M"),
            }
        )

    with open(nazev_souboru, "w", encoding="utf-8") as soubor:
        json.dump(export, soubor, ensure_ascii=False, indent=2)

    console.print(f"[green]Data byla uložena do JSON souboru: {nazev_souboru}[/green]")


def main():
    data = nacti_data("dochazka.csv")
    uloz_data_json(data)

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