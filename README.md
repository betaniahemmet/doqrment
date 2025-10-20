# Doqrment

*English summary below*

Ett lättviktigt, mobilförst system för att logga subjektiva observationer (t.ex. humör, energi, beteenden) i LSS‑boenden och daglig verksamhet. Byggt med Flask, React och SQLite.

## Funktioner
- Mobilvänlig loggning via QR‑koder
- Adminvy för att skapa mätningar (vecka/månad)
- Lagring i SQLite med enkel export
- Rapporter och diagram
- (Beta) Automatisk e‑post av rapporter

## Kom igång

```bash
# 1) Klona
git clone https://github.com/betaniahemmet/doqrment.git
cd doqrment

# 2) Backend (Flask)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3) Initiera databas
python setup_db.py

# 4) Frontend (React)
npm install --prefix app/components
npm run build --prefix app/components   # output -> app/static/

# 5) Starta
flask run
# Öppna: http://localhost:5000
```

> Tips: Använd en `.env` för miljövariabler (t.ex. `FLASK_ENV=development`).

## Stack / Arkitektur
- **Backend:** Flask + SQLAlchemy
- **Frontend:** React + Tailwind (Vite)
- **Databas:** SQLite
- **QR/PDF:** fpdf, qrcode
- **Drift:** Lokalt eller via Docker (valfritt)

## Status
Aktiv utveckling

## License
Detta projekt är licensierat under **MIT** – se den org‑gemensamma licensen:
https://github.com/betaniahemmet/.github/blob/main/LICENSE

## Kontakt
Öppna ett issue eller mejla: henrik.bjorserud@betaniahemmet.se

---

## English Summary

Doqrment is a mobile‑first logging system for subjective observations (e.g., mood, energy, behaviors) in care settings (LSS/day activity centers). Built with Flask, React, and SQLite.

**Key features:** QR‑based logging, admin view to create sessions (week/month), SQLite storage, basic charts/reports, optional email reports.

**Quick start:** See the Swedish section above for step‑by‑step setup.
