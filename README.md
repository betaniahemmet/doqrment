# Doqrment – Tracking System for Care Environments

**Doqrment** is a lightweight, mobile-first system for tracking subjective observations (e.g., mood, energy, behavior) in care settings like LSS group homes or daily activity centers. Built with Flask, React, and SQLite, it enables structured data collection and automated reporting.

## Features

- 📱 Mobile-friendly logging UI via QR code  
- 🛠️ Admin interface for setting up tracking sessions  
- 🗃️ Data stored in SQLite with simple export options  
- 🗓️ Weekly or monthly durations  
- 📈 Auto-generated visualizations (line charts, boxplots, event markers)  
- 📤 Optional report emailing (beta)

## Tech Stack

- **Backend**: Flask + SQLAlchemy  
- **Frontend**: React + Tailwind CSS (via Vite)  
- **Database**: SQLite  
- **QR Codes**: `fpdf`, `qrcode`  
- **Charts**: Matplotlib, Seaborn  
- **Deployment**: Docker-ready

## Project Structure

- `app/`  
  - `components/` – React frontend components  
  - `static/` – Build output from Vite  
  - `templates/` – HTML files  
  - `utils/qr_pdf.py` – QR code + PDF generation  
  - `models.py` – SQLAlchemy models  
  - `routes.py` – Flask routes  
- `instance/doqrment.sqlite` – SQLite database (auto-created)

## Setup Instructions

### 1. Clone the Repo

```
git clone https://github.com/your-org/doqrment.git
cd doqrment
```

### 2. Backend Setup (Flask)

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialize Database

```
python setup_db.py
```

(This will create the `doqrment.sqlite` file in the `instance/` folder.)

### 4. Frontend Setup (React)

```
cd app/components/
npm install
npm run build
```

(This builds the frontend and outputs to `../static/`.)

### 5. Run Development Server

```
cd ../..
flask run
```

Access the app at: [http://localhost:5000](http://localhost:5000)

## Docker (Optional)

_Coming soon – Dockerfile present but not fully configured yet._

## License

MIT
