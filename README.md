# Ticket Tracker (SQL + Python)

A portfolio project simulating a real-world IT helpdesk ticketing system built with SQLite and Python.

The project tracks support tickets submitted by employees, the technicians who resolve them, and the devices assigned to each user. It also includes analytical SQL queries answering common IT support questions, such as technician workload, average resolution time, SLA breaches, and monthly ticket trends. A Python script automates report generation by exporting query results to CSV files and creating charts.

## Database structure

The database consists of five related tables:

- **users** – employees who submit support tickets
- **technicians** – IT staff responsible for resolving tickets
- **tickets** – the main table containing ticket information
- **ticket_comments** – ticket history and technician notes
- **assets** – devices assigned to users (laptops, monitors, etc.)

```
users --< tickets >-- technicians
  |           |
  |           +--< ticket_comments
  |
  +--< assets
```

## Skills demonstrated

- Relational database design
- SQL JOINs
- Aggregate functions
- CASE expressions
- Window functions (LAG)
- SQLite
- Python automation
- CSV report generation
- Data visualization with Matplotlib

## Files

- **schema.sql** – database schema and table definitions
- **seed_data.py** – generates around 450 realistic sample tickets with randomized users, dates, priorities, and statuses
- **queries.sql** – analytical SQL queries demonstrating JOINs, aggregations, CASE expressions, and window functions
- **report.py** – executes SQL queries and exports CSV reports and PNG charts
- **requirements.txt** – project dependencies
- **.gitignore** – Git configuration

## Example queries

- Average resolution time by priority using `julianday()`
- Technician performance summary based on resolved tickets
- Month-over-month ticket trend using the `LAG()` window function
- SLA breach detection based on ticket priority and resolution time
- Ticket distribution by status and priority

The complete collection of queries is available in `queries.sql`.

## How to run

Requires Python 3.

```bash
pip install -r requirements.txt
python3 seed_data.py
python3 report.py
```

Running the scripts will:

- generate the SQLite database (`helpdesk.db`)
- populate it with sample data
- create CSV reports
- generate charts in the `reports/` directory

To explore the database manually, open `helpdesk.db` with DB Browser for SQLite and execute any query from `queries.sql`.

## Sample output

![Tickets by status](screenshots/tickets_by_status.png)

![Monthly trend](screenshots/monthly_trend.png)

## Possible extensions

- Migrate the database from SQLite to PostgreSQL
- Add data validation tests (for example, ensuring `resolved_at` is never earlier than `created_at`)
- Build a simple dashboard using Flask
- Optimize query performance with indexes
- Connect the project with a log parser so real log events can automatically generate support tickets
