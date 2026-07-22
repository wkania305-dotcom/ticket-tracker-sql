-- ============================================================
-- HELPDESK TICKETING SYSTEM - SCHEMA
-- Autor: Wiktoria Kania
-- Opis: Baza danych symulujaca system zgloszen IT Support
-- ============================================================

DROP TABLE IF EXISTS ticket_comments;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS technicians;
DROP TABLE IF EXISTS users;

-- Pracownicy zglaszajacy problemy
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    department  TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE
);

-- Technicy IT obslugujacy zgloszenia
CREATE TABLE technicians (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    team        TEXT NOT NULL       -- np. Network, Hardware, Software
);

-- Sprzet przypisany do pracownikow
CREATE TABLE assets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    device_type     TEXT NOT NULL,      -- Laptop, Monitor, Printer, Phone
    serial_number   TEXT NOT NULL UNIQUE,
    purchase_date   DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Zgloszenia (glowna tabela)
CREATE TABLE tickets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    technician_id   INTEGER,                       -- moze byc NULL, jesli nieprzypisany
    subject         TEXT NOT NULL,                 -- krotki opis problemu
    category        TEXT NOT NULL,                 -- Network, Hardware, Software, Account, Other
    priority        TEXT NOT NULL,                 -- Low, Medium, High, Critical
    status          TEXT NOT NULL,                 -- Open, In Progress, Resolved, Closed
    created_at      DATETIME NOT NULL,
    resolved_at     DATETIME,                      -- NULL, jesli nierozwiazane
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (technician_id) REFERENCES technicians(id)
);

-- Komentarze / historia obslugi zgloszenia
CREATE TABLE ticket_comments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL,
    author      TEXT NOT NULL,
    comment     TEXT NOT NULL,
    created_at  DATETIME NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);

-- Indeksy przyspieszajace najczestsze zapytania
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
CREATE INDEX idx_tickets_technician ON tickets(technician_id);
