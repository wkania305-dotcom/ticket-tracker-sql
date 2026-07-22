# IT Helpdesk Ticketing System — SQL + Python Analytics

Projekt symuluje bazę danych systemu zgłoszeń IT (helpdesk), jakiego używa
każdy dział IT Support. Zawiera relacyjny model danych w SQL, generator
realistycznych danych testowych oraz skrypt w Pythonie, który automatycznie
tworzy raporty CSV i wykresy na podstawie zapytań SQL.

## Czego dotyczy ten projekt

Dział IT Support obsługuje setki zgłoszeń miesięcznie: awarie sprzętu,
problemy z siecią, resety haseł itd. Ten projekt odpowiada na pytania,
które realnie zadaje sobie taki zespół:

- Ile zgłoszeń mamy w każdym statusie?
- Jak szybko rozwiązujemy zgłoszenia w zależności od priorytetu?
- Który technik obsługuje najwięcej zgłoszeń?
- Które zgłoszenia przekraczają SLA (umowny czas reakcji)?
- Jak zmienia się liczba zgłoszeń w czasie?

## Struktura bazy danych (ERD)

```
users (id, name, department, email)
        │
        ├──< tickets (id, user_id, technician_id, subject, category,
        │             priority, status, created_at, resolved_at)
        │             │
        │             └──< ticket_comments (id, ticket_id, author, comment, created_at)
        │
        └──< assets (id, user_id, device_type, serial_number, purchase_date)

technicians (id, name, team) ──< tickets
```

## Struktura plików w repozytorium

```
helpdesk-project/
├── schema.sql          -> definicja tabel i indeksów
├── seed_data.py         -> generuje dane testowe i tworzy helpdesk.db
├── queries.sql           -> 10 gotowych zapytan analitycznych z komentarzami
├── report.py              -> laczy sie z baza, eksportuje CSV + wykresy PNG
├── reports/                -> (generowane automatycznie) pliki CSV
│   └── charts/               -> (generowane automatycznie) wykresy PNG
└── README.md
```

## Jak uruchomić projekt u siebie — krok po kroku

### Krok 0: Sprawdź, czy masz Pythona
Otwórz terminal (Windows: wpisz w wyszukiwarce "PowerShell" albo "cmd";
Mac: wpisz w Spotlight "Terminal") i wpisz:
```
python3 --version
```
Jeśli pokaże np. `Python 3.11.x` — masz Pythona i możesz przejść dalej.
Jeśli nie — pobierz go z [python.org/downloads](https://www.python.org/downloads/)
i podczas instalacji **zaznacz checkbox "Add Python to PATH"**.

### Krok 1: Pobierz pliki projektu
Jeśli masz już to repozytorium na GitHubie (patrz sekcja niżej), pobierz je poleceniem:
```
git clone https://github.com/TWOJA-NAZWA-UZYTKOWNIKA/helpdesk-project.git
cd helpdesk-project
```
Jeśli pracujesz lokalnie z plikami, które właśnie dostałaś — po prostu wejdź
do folderu z tymi plikami w terminalu, np.:
```
cd Downloads/helpdesk-project
```

### Krok 2: Zainstaluj potrzebną bibliotekę (tylko do wykresów)
```
pip install matplotlib --break-system-packages
```
(Jeśli to polecenie da błąd, spróbuj bez `--break-system-packages`,
albo `pip3 install matplotlib`)

### Krok 3: Wygeneruj bazę danych z przykładowymi zgłoszeniami
```
python3 seed_data.py
```
Powinnaś zobaczyć komunikat, że baza `helpdesk.db` została utworzona
z ok. 450 zgłoszeniami, 60 użytkownikami itd.

### Krok 4: Wygeneruj raporty i wykresy
```
python3 report.py
```
To stworzy folder `reports/` z plikami CSV oraz `reports/charts/` z wykresami PNG.
Możesz je otworzyć zwykłym podglądem zdjęć / Excelem.

### Krok 5 (opcjonalnie): Uruchom pojedyncze zapytania SQL
Jeśli chcesz "pobawić się" zapytaniami bez Pythona, zainstaluj DB Browser
for SQLite (darmowy program): [sqlitebrowser.org](https://sqlitebrowser.org/)
1. Otwórz program → "Open Database" → wybierz plik `helpdesk.db`
2. Przejdź do zakładki "Execute SQL"
3. Wklej dowolne zapytanie z pliku `queries.sql` i kliknij "Execute" (▶)

## Jak wrzucić ten projekt na GitHub (żeby rekruter mógł go zobaczyć)

1. Załóż konto na [github.com](https://github.com), jeśli jeszcze nie masz.
2. Kliknij zielony przycisk **"New"** (lub "+" w prawym górnym rogu → "New repository").
3. Nazwa repozytorium: `helpdesk-ticketing-sql` (albo dowolna sensowna nazwa).
4. Ustaw jako **Public** (żeby rekruter mógł zobaczyć bez logowania).
5. NIE zaznaczaj "Add README" (Ty już masz swój plik README.md).
6. Kliknij "Create repository".
7. Na następnej stronie GitHub pokaże Ci komendy do wklejenia w terminalu.
   W folderze z projektem wpisz kolejno:
```
git init
git add .
git commit -m "Pierwsza wersja: helpdesk ticketing system SQL + Python"
git branch -M main
git remote add origin https://github.com/TWOJA-NAZWA-UZYTKOWNIKA/helpdesk-ticketing-sql.git
git push -u origin main
```
8. Odśwież stronę repozytorium na GitHubie — wszystkie pliki powinny się pojawić.

**Ważne:** plik `helpdesk.db` i folder `reports/` to dane wygenerowane —
nie musisz ich wrzucać na GitHub (można je łatwo odtworzyć poleceniem
`python3 seed_data.py && python3 report.py`). Możesz dodać plik `.gitignore`
z zawartością:
```
helpdesk.db
reports/
```
żeby git ich nie śledził. Zamiast tego wrzuć 1-2 przykładowe wykresy PNG
do repo (np. do folderu `screenshots/`), żeby rekruter widział efekt
bez klonowania i uruchamiania projektu.

## Co warto dodać do opisu repozytorium na GitHubie

W polu "About" repozytorium (ikonka zębatki obok "About" po prawej stronie)
wpisz krótki opis, np.:
> SQL + Python project simulating an IT helpdesk ticketing system — schema design, analytical queries (JOINs, window functions, CASE), and automated CSV/chart reporting.

Dodaj też tagi (topics): `sql`, `sqlite`, `python`, `data-analysis`, `it-support`

## Możliwe rozszerzenia (jeśli chcesz pójść dalej)

- Przenieś bazę z SQLite do PostgreSQL, żeby pokazać pracę z "prawdziwym" serwerem bazodanowym
- Dodaj prosty dashboard w Streamlit (`pip install streamlit`) zamiast plików PNG
- Dodaj testy sprawdzające poprawność danych (np. czy `resolved_at` zawsze jest po `created_at`)
- Połącz z Twoim istniejącym projektem **Linux Log Parser** — logi mogą trafiać
  jako nowe rekordy do tabeli `tickets` zamiast tylko do konsoli

## Autor

Wiktoria Kania — projekt stworzony jako część przygotowań do rekrutacji na
stanowisko IT Support / Infrastructure Intern.
