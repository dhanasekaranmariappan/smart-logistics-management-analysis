# 🚚 Smart Logistics Management & Analytics Platform

A centralized logistics analytics platform built with Python, MySQL, and Streamlit.

## 📊 Features
- KPI Overview Dashboard
- Shipment Search & Filtering
- Courier Performance Analytics
- Cost Analytics

## 🛠️ Tech Stack
- **Language:** Python
- **Database:** MySQL
- **Dashboard:** Streamlit
- **Libraries:** Pandas, SQLAlchemy, Plotly

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/dhanasekaranmariappan/smart-logistics-management-analytics.git
cd smart-logistics-management-analytics

### 2. Install dependencies
pip install -r requirements.txt

### 3. Configure environment variables
Create a `.env` file in the root directory:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_PORT=3306
DB_NAME=your_database_name

### 4. Load data into MySQL
python load_data.py

### 5. Run the app
streamlit run smart-logistics-app.py

## 📁 Project Structure
smart-logistics-management-analytics/
├── smart-logistics-app.py   # Main entry point
├── shared_db.py             # Database connection
├── sidebar.py               # Shared sidebar
├── load_data.py             # Data loading script
├── requirements.txt         # Dependencies
├── .env                     # Environment variables (not tracked)
├── .gitignore
├── README.md
└── pages/
    ├── 1_KPI_Overview.py
    ├── 2_Shipment_Search.py
    ├── 3_Courier_Performance.py
    └── 4_Cost_Analytics.py