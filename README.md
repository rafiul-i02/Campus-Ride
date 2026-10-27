# 🚌 PUB CampusRide - Pundra University Transport Portal

> **Demo Video Link:** https://drive.google.com/file/d/1xQFHxYIkpo04YTyv-9MolI1z1YMHspXz/view?usp=drive_link
> **Live Deployment Link:** https://4cbbdf23-0f01-4a95-86f5-c97e96dbca0b-00-3talj33c890kk.pike.replit.dev/

---

## 📌 Project Overview
**PUB CampusRide** is a full-stack web application built to streamline transport and route management for the students and administration of Pundra University of Science & Technology. It enables students to manage bus routes, schedules, live ETAs, and travel intentions, while administrators and dispatchers handle bus fleets, drivers, maintenance, and urgent announcements.

* **Problem ID:** PUB-CSE-Fest-Hackathon-C4
* **Team Name:** Pentabyte
* **Team Members:**
  1. Sanghamitra Pandit (Student ID: 03226105101008) - Team Leader
  2. Rafiul Islam (Student ID: 03226105101022) - Backend Developer
  3. Shahriyar Shawon (Student ID: ) - Script Writer
  4. Bariul Bappy (Student ID: 03226105101006) - Frontend & UI/UX
  5. Shahed Kamal (Student ID: 03226105101016) - Video Editor

---

## 🛠️ Technology Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript (Responsive UI)
* **Hosting / Deployment:** Replit
* **Version Control:** GitHub

---

## 📋 Feature Status Table

| Feature Name | Status | Description |
| :--- | :---: | :--- |
| **User Authentication & Roles** | ✅ Done | Admin, Dispatcher, and Student portals. |
| **Urgent Notice Board** | ✅ Done | Live urgent notice publishing and front-page updates. |
| **Route Management** | ✅ Done | Route management with ordered stops, timing, and pickup instructions. |
| **Bus Schedule (Routine)** | ✅ Done | Weekly routine-based public bus schedules. |
| **Driver Management & Privacy** | ✅ Done | Driver information management with phone number privacy masking. |
| **Bus Management** | ✅ Done | Fleet bus and vehicle status tracking. |
| **Trip Scheduling & Overlap Detection** | ✅ Done | Recurring and one-off trip scheduling with double-booking conflict prevention. |
| **Dispatcher Portal & ETA** | ✅ Done | Departure, stop arrival, delay logging, and Estimated Time of Arrival (ETA). |
| **Breakdown & Replacement Finder** | ✅ Done | Automatic alternative bus/driver finder or capacity shortage flagging. |
| **Trip History & Analytics Reports** | ✅ Done | Comprehensive logs on delays, cancellations, and vehicle usage rates. |
| **Passenger Feedback & Incidents** | ✅ Done | Feedback, complaints, and incident tracking system with resolution status. |
| **Maintenance Tracking** | ✅ Done | Vehicle maintenance needs and follow-up tracking to resolution. |
| **Student Portal & Demand Analysis** | ✅ Done | Preferred route saving, travel intention submission, and demand vs. capacity analysis. |

---

## 🚀 Local Setup & Run Instructions
Follow these steps to run the project locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/rafiul-i02/Campus-Ride.git](https://github.com/rafiul-i02/Campus-Ride.git)
   cd Campus-Ride

Install Dependencies:

Bash
pip install -r requirements.txt

Run the Application:

Bash
python main.py

Open your browser and go to: http://192.168.0.201:5000/

🔑 Sample Login / Test Accounts
All features across admin, dispatcher, and student portals can be tested in real-time directly via the navigation bar tabs.

📸 Screenshots & Architecture
Dashboard & Live Notice

Dispatcher & ETA Panel

Student Demand vs Capacity Analytics

⚠️ Known Limitations
Currently utilizes in-memory data structures, which reset upon application restart.

👥 Team Contribution
Rafiul Islam: Backend Development (Flask Backend, API Endpoints & Deployment)

Other Members: UI/UX Design, Feature planning, data collection, testing, and presentation preparation.
