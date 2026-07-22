"""
seed_data.py
-------------
Generuje realistyczne dane testowe i wypelnia baze helpdesk.db.
Nie wymaga zadnych zewnetrznych bibliotek (samo Python standard library),
zeby uruchomienie bylo tak proste, jak to mozliwe.

Uzycie:
    python3 seed_data.py
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_FILE = "helpdesk.db"
SCHEMA_FILE = "schema.sql"

random.seed(42)  # stale ziarno losowosci -> powtarzalne wyniki przy kazdym uruchomieniu

# ---------------------------------------------------------------
# Dane bazowe do losowania
# ---------------------------------------------------------------
FIRST_NAMES = ["Anna", "Piotr", "Katarzyna", "Tomasz", "Magdalena", "Michal",
               "Agnieszka", "Krzysztof", "Ewa", "Lukasz", "Joanna", "Marek",
               "Natalia", "Pawel", "Aleksandra", "Grzegorz", "Monika", "Adam",
               "Karolina", "Rafal"]
LAST_NAMES = ["Nowak", "Kowalski", "Wisniewski", "Wojcik", "Kowalczyk",
              "Kaminski", "Lewandowski", "Zielinski", "Szymanski", "Wozniak",
              "Dabrowski", "Kozlowski", "Jankowski", "Mazur", "Krawczyk"]
DEPARTMENTS = ["Sales", "Marketing", "Finance", "HR", "Operations",
               "Engineering", "Customer Service", "Legal"]
TEAMS = ["Network", "Hardware", "Software", "Security"]
TECH_FIRST = ["Wiktoria", "Bartosz", "Sylwia", "Dominik", "Klaudia", "Filip"]
TECH_LAST = ["Zajac", "Baran", "Sobczak", "Wrobel", "Malinowski", "Pawlak"]

CATEGORIES = ["Network", "Hardware", "Software", "Account", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
DEVICE_TYPES = ["Laptop", "Monitor", "Printer", "Phone", "Docking Station"]

# Gotowe szablony tresci zgloszen - dzieki temu dane wygladaja realistycznie
TICKET_TEMPLATES = {
    "Network": ["Brak dostepu do internetu", "VPN nie laczy sie z serwerem",
                "Wolne polaczenie sieciowe", "Problem z Wi-Fi w biurze"],
    "Hardware": ["Laptop nie wlacza sie", "Monitor miga i gasnie",
                 "Drukarka zacina papier", "Klawiatura nie dziala poprawnie"],
    "Software": ["Aplikacja X sie zawiesza", "Blad przy instalacji programu",
                 "System operacyjny wymaga aktualizacji", "Excel zamyka sie po otwarciu pliku"],
    "Account": ["Nie moge zalogowac sie na konto", "Prosba o reset hasla",
                "Konto zablokowane po zbyt wielu probach logowania",
                "Brak dostepu do wspolnego dysku"],
    "Other": ["Prosba o nowy sprzet", "Pytanie o procedure IT",
              "Zgloszenie ogolne", "Prosba o instalacje dodatkowego oprogramowania"],
}

COMMENT_TEMPLATES = [
    "Zgloszenie przyjete, rozpoczynam diagnoze.",
    "Poproszono uzytkownika o dodatkowe informacje.",
    "Zidentyfikowano przyczyne problemu.",
    "Wykonano restart urzadzenia, problem ustapil.",
    "Przekazano zgloszenie do zespolu Network.",
    "Zainstalowano aktualizacje, sprawdzam efekt.",
    "Uzytkownik potwierdzil, ze problem zostal rozwiazany.",
    "Zamykam zgloszenie po weryfikacji.",
]

N_USERS = 60
N_TECHNICIANS = 8
N_ASSETS = 90
N_TICKETS = 450
DAYS_RANGE = 365  # dane z ostatniego roku


def random_date(days_back):
    return datetime.now() - timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def build_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 1. Wczytaj i wykonaj schema.sql (tworzy / czysci tabele)
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    # 2. Uzytkownicy
    users = []
    for i in range(N_USERS):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        dept = random.choice(DEPARTMENTS)
        email = f"user{i+1}@firma.pl"
        users.append((name, dept, email))
    cur.executemany("INSERT INTO users (name, department, email) VALUES (?, ?, ?)", users)

    # 3. Technicy
    technicians = []
    for i in range(N_TECHNICIANS):
        name = f"{random.choice(TECH_FIRST)} {random.choice(TECH_LAST)}"
        team = random.choice(TEAMS)
        technicians.append((name, team))
    cur.executemany("INSERT INTO technicians (name, team) VALUES (?, ?)", technicians)

    # 4. Sprzet (assets)
    assets = []
    for i in range(N_ASSETS):
        user_id = random.randint(1, N_USERS)
        device = random.choice(DEVICE_TYPES)
        serial = f"SN-{10000 + i}"
        purchase = (datetime.now() - timedelta(days=random.randint(30, 1500))).date().isoformat()
        assets.append((user_id, device, serial, purchase))
    cur.executemany(
        "INSERT INTO assets (user_id, device_type, serial_number, purchase_date) VALUES (?, ?, ?, ?)",
        assets)

    # 5. Zgloszenia (tickets) + komentarze
    tickets = []
    for i in range(N_TICKETS):
        user_id = random.randint(1, N_USERS)
        category = random.choice(CATEGORIES)
        subject = random.choice(TICKET_TEMPLATES[category])
        priority = random.choices(PRIORITIES, weights=[35, 35, 22, 8])[0]
        created_at = random_date(DAYS_RANGE)

        status = random.choices(STATUSES, weights=[10, 15, 30, 45])[0]
        technician_id = None
        resolved_at = None

        if status in ("In Progress", "Resolved", "Closed"):
            technician_id = random.randint(1, N_TECHNICIANS)

        if status in ("Resolved", "Closed"):
            # czas rozwiazania zalezny od priorytetu (Critical -> szybciej)
            resolve_hours = {
                "Critical": random.uniform(1, 12),
                "High": random.uniform(4, 48),
                "Medium": random.uniform(12, 96),
                "Low": random.uniform(24, 168),
            }[priority]
            resolved_at = created_at + timedelta(hours=resolve_hours)
            # nie pozwalamy na date rozwiazania w przyszlosci
            if resolved_at > datetime.now():
                resolved_at = datetime.now()

        tickets.append((
            user_id, technician_id, subject, category, priority, status,
            created_at.isoformat(sep=" ", timespec="seconds"),
            resolved_at.isoformat(sep=" ", timespec="seconds") if resolved_at else None,
        ))

    cur.executemany("""
        INSERT INTO tickets (user_id, technician_id, subject, category, priority, status, created_at, resolved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, tickets)

    # 6. Komentarze do czesci zgloszen (1-3 na ticket, dla tych ktore maja technika)
    cur.execute("SELECT id, technician_id, created_at FROM tickets WHERE technician_id IS NOT NULL")
    ticket_rows = cur.fetchall()

    comments = []
    for ticket_id, technician_id, created_at in ticket_rows:
        base_time = datetime.fromisoformat(created_at)
        n_comments = random.randint(1, 3)
        for c in range(n_comments):
            comment_time = base_time + timedelta(hours=random.uniform(0.5, 20) * (c + 1))
            author = f"Technician #{technician_id}"
            comments.append((ticket_id, author, random.choice(COMMENT_TEMPLATES),
                              comment_time.isoformat(sep=" ", timespec="seconds")))
    cur.executemany("""
        INSERT INTO ticket_comments (ticket_id, author, comment, created_at)
        VALUES (?, ?, ?, ?)
    """, comments)

    conn.commit()
    conn.close()

    print(f"Baza '{DB_FILE}' zostala utworzona i wypelniona danymi:")
    print(f"  - {N_USERS} uzytkownikow")
    print(f"  - {N_TECHNICIANS} technikow")
    print(f"  - {N_ASSETS} sprzetow")
    print(f"  - {N_TICKETS} zgloszen")
    print(f"  - {len(comments)} komentarzy")


if __name__ == "__main__":
    build_database()
