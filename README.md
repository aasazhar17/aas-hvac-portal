# AAS Air Conditioning & Engineering - Full Stack HVAC Portal

A premium, enterprise-grade B2B web application for **AAS Air Conditioning & Engineering**, modeled after Fortune 500 engineering leaders. It is fully integrated with a Python FastAPI backend, a SQLite database, and a secure Admin Dashboard portal.

## 🚀 Key Features
- **Modern Responsive Design**: Perfect styling compatibility across Mobile, Tablet, and Desktop displays.
- **Light & Dark Theme Switcher**: Variable-driven theme toggle that persists selections in `localStorage`.
- **Chilling Capacity Calculator**: Dynamic ton-of-refrigeration (TR) estimator that recommends matching chilling lines based on fluid parameters.
- **Smart Assistant Chatbot**: Integrated backend NLP-based chat agent that maps user queries to catalog specifications and logs transcripts.
- **Lead Tracking Database**: Captures catalog download requests and quotation inquiries.
- **Operations Admin Dashboard**: Secured dashboard (`/admin`) displaying tables of inquiries, catalog registrants, and chatbot dialogs in real-time.

---

## 🔑 Administrative Access
- **Admin Panel URL**: `http://localhost:8000/admin`
- **Dashboard Security Passkey**: `AAS_ADMIN_2026`

*To change the password, update the `ADMIN_SECURE_TOKEN` value in [main.py](file:///c:/Users/Azhar/OneDrive/Attachments/Desktop/AAS%20AIRCONDITIONING%20AND%20ENGINEERING/main.py).*

---

## 💻 Local Development Setup

1. **Install Dependencies**:
   Ensure you have Python 3 installed. Open your terminal in the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Development Server**:
   ```bash
   uvicorn main:app --reload
   ```
   Open **[http://localhost:8000](http://localhost:8000)** in your browser to view the live website.

---

## ☁️ Deployment Guidelines (A to Z)

To deploy this website live for free (e.g., using **Render.com**):

1. **Upload to GitHub**:
   Initialize a git repository in this folder, commit all files (including `/static`, `main.py`, `database.py`, `requirements.txt`, and `Procfile`), and push to a private or public GitHub repository.

2. **Create Render Web Service**:
   - Log into [Render.com](https://render.com) and click **New > Web Service**.
   - Connect your GitHub repository.
   - Configure the following settings:
     - **Name**: `aas-hvac-portal`
     - **Environment**: `Python`
     - **Branch**: `main`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click **Create Web Service**.

Render will automatically run the build script, execute `main.py` (which initializes the SQLite database file `database.db` automatically), and host your portal on a public domain!
