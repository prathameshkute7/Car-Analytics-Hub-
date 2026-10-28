# 🚘 CAR ANALYTICS HUB

> An interactive, high-performance automotive web dashboard for real-time vehicle research, performance visualization, and side-by-side specification analysis.

---

## ✨ Key Features

* 🏷️ **Dynamic Brand Filter** — Instantly filter models by manufacturer without page reloads.
* 📊 **Performance Visualizers** — Animated progress meters for Horsepower, Top Speed, and Efficiency[cite: 2, 5].
* ⚔️ **Comparison Matrix** — Side-by-side feature and spec comparison between any two vehicles[cite: 2, 3].
* 📉 **Interactive Analytics** — Dynamic Chart.js scatter plots analyzing Horsepower vs. Fuel Efficiency[cite: 3, 4].
* 📱 **Responsive Dark UI** — Modern, sleek Bootstrap 5 interface tailored for all screen sizes[cite: 2, 5].

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.x, Flask REST API[cite: 2] |
| **Frontend** | HTML5, CSS3, Bootstrap 5[cite: 2] |
| **Client-Side Logic** | Vanilla JavaScript (ES6), Asynchronous Fetch API[cite: 2, 6] |
| **Data Visualization** | Chart.js[cite: 3] |

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
Ensure you have **Python 3.x** installed on your system.

### 2️⃣ Installation & Setup

Clone the repository and navigate to the project directory:
```bash
git clone [https://github.com/your-username/car-analytics-hub.git](https://github.com/your-username/car-analytics-hub.git)
cd car-analytics-hub

### 1. Install dependencies

Install the required backend dependencies:

```bash
pip install flask
```

### 2. Run the server

Run the Flask development server:

```bash
python app.py
```

### 3. Open the app

Open your browser and visit:


[🌐 Visit Website](https://car-analytics-hub.onrender.com)

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/get_all_data` | GET | Retrieves the full dataset of vehicle specifications. |
| `/get_data?brand=` | GET | Retrieves filtered vehicle records by brand name. |

## 🔮 Future Enhancements

- 🗄️ Integration with persistent databases (PostgreSQL / MongoDB)
- 🔐 Admin panel with authentication and role-based access control
- 📄 Exportable PDF comparison reports and analytics summaries
