"""
report.py
----------
Laczy sie z baza helpdesk.db, uruchamia zapytania analityczne
i generuje:
  1. Raporty CSV w folderze reports/
  2. Wykresy PNG w folderze reports/charts/

To pokazuje umiejetnosc laczenia SQL z automatyzacja w Pythonie -
dokladnie to, czego szuka sie na stanowiskach IT Support / Junior Data.

Uzycie:
    python3 report.py
"""

import sqlite3
import csv
import os
import matplotlib
matplotlib.use("Agg")  # zapisujemy wykresy do pliku, nie otwieramy okna
import matplotlib.pyplot as plt

DB_FILE = "helpdesk.db"
REPORTS_DIR = "reports"
CHARTS_DIR = os.path.join(REPORTS_DIR, "charts")


def ensure_dirs():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)


def run_query(cur, query):
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return columns, rows


def save_csv(filename, columns, rows):
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"  zapisano: {path}")


def chart_tickets_by_status(cur):
    columns, rows = run_query(cur, """
        SELECT status, COUNT(*) FROM tickets GROUP BY status ORDER BY 2 DESC
    """)
    save_csv("tickets_by_status.csv", columns, rows)

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color="#4C72B0")
    plt.title("Liczba zgloszen wg statusu")
    plt.ylabel("Liczba zgloszen")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "tickets_by_status.png"))
    plt.close()
    print("  wykres: tickets_by_status.png")


def chart_avg_resolution_time(cur):
    columns, rows = run_query(cur, """
        SELECT priority,
               ROUND(AVG((julianday(resolved_at) - julianday(created_at)) * 24), 1) AS avg_hours
        FROM tickets
        WHERE resolved_at IS NOT NULL
        GROUP BY priority
        ORDER BY CASE priority
            WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4 END
    """)
    save_csv("avg_resolution_time.csv", columns, rows)

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color="#C44E52")
    plt.title("Sredni czas rozwiazania zgloszenia (godziny)")
    plt.ylabel("Godziny")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "avg_resolution_time.png"))
    plt.close()
    print("  wykres: avg_resolution_time.png")


def chart_monthly_trend(cur):
    columns, rows = run_query(cur, """
        SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS total
        FROM tickets
        GROUP BY month
        ORDER BY month
    """)
    save_csv("monthly_trend.csv", columns, rows)

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    plt.figure(figsize=(8, 4))
    plt.plot(labels, values, marker="o", color="#55A868")
    plt.title("Liczba nowych zgloszen w czasie")
    plt.ylabel("Liczba zgloszen")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "monthly_trend.png"))
    plt.close()
    print("  wykres: monthly_trend.png")


def technician_leaderboard(cur):
    columns, rows = run_query(cur, """
        SELECT t.name, t.team, COUNT(tk.id) AS resolved
        FROM technicians t
        JOIN tickets tk ON tk.technician_id = t.id
        WHERE tk.status IN ('Resolved', 'Closed')
        GROUP BY t.id
        ORDER BY resolved DESC
    """)
    save_csv("technician_leaderboard.csv", columns, rows)


def sla_breaches(cur):
    columns, rows = run_query(cur, """
        SELECT id, subject, priority, status, created_at,
               ROUND((julianday('now') - julianday(created_at)) * 24, 1) AS hours_open
        FROM tickets
        WHERE status IN ('Open', 'In Progress')
          AND (
                (priority = 'Critical' AND (julianday('now') - julianday(created_at)) * 24 > 4)
             OR (priority = 'High' AND (julianday('now') - julianday(created_at)) * 24 > 24)
          )
        ORDER BY hours_open DESC
    """)
    save_csv("sla_breaches.csv", columns, rows)


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    print("Generowanie raportow...")
    chart_tickets_by_status(cur)
    chart_avg_resolution_time(cur)
    chart_monthly_trend(cur)
    technician_leaderboard(cur)
    sla_breaches(cur)

    conn.close()
    print("\nGotowe! Sprawdz folder 'reports/' (CSV) oraz 'reports/charts/' (wykresy PNG).")


if __name__ == "__main__":
    main()
