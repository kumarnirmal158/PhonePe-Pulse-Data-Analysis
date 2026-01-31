**📊 PhonePe Pulse Data Analysis & Visualization Dashboard**

**🧾 Project Overview**

This project is an end-to-end data analytics and visualization application built using PhonePe Pulse open data.
It extracts large-scale JSON data, transforms it into structured tables, stores it in SQLite, and presents interactive dashboards and business insights using Streamlit and Plotly.
The project focuses on user behavior, transactions, device dominance, registrations, and insurance adoption across India.

**🎯 Objectives**
1) Extract and process PhonePe Pulse JSON datasets
2) Store structured data in a relational SQLite database
3) Build an interactive Streamlit dashboard
4) Perform business case studies with insights & recommendations
5) Enable state, district, pincode-level analysis
6) Present insights visually for decision-making

**🛠️ Tech Stack**

| Category        | Tools               |
| --------------- | ------------------- |
| Language        | Python              |
| Data Processing | Pandas, JSON        |
| Database        | SQLite              |
| Visualization   | Plotly, Matplotlib  |
| Dashboard       | Streamlit           |
| Mapping         | GeoJSON (India Map) |

📁 Project Structure

PhonePe-Pulse-Analysis/                                                                                                                                                                       
│                                                                                                                                                                                                          
├── Phonepe_Project_1.py       # JSON extraction, DataFrame creation, # SQLite table creation & insertion                                                                                 
│                                                                                                                                                                                                            
├── Phonepe_project.db         # SQLite database                                                                                                                                                               
│                                                                                                                                                                                                
├── app.py                     # Main Streamlit dashboard                                                                                                                                                       
├── business_case.py           # Business case study analysis                                                                                                                                                    
│                                                                                                                                                                                                    
├── utils/                                                                                                                                                                                     
│   └── db.py                  # Database connection utility                                                                                                                                               
│                                                                                                                                                                                                
└── README.md                  # Project documentation                                                                                                                                               


**🗂️ Data Sources**
Data is sourced from PhonePe Pulse GitHub Repository:
1) Aggregated Transactions
2) Aggregated Users
3) Aggregated Insurance
4) Map Transactions
5) Map Users
6) Map Insurance
7) Top Transactions
8) Top Users
9) Top Insurance
Each dataset is extracted from state → year → quarter JSON hierarchy.

**🧱 Database Schema**

The project uses SQLite with the following tables:
1) Agg_Tran – Aggregated transactions
2) Agg_user – Device brand & user data
3) Agg_ins – Aggregated insurance data
4) map_trans – District-level transactions
5) map_users – User registrations & app opens
6) map_ins – District-level insurance data
7) top_trans – Top districts & pincodes (transactions)
8) top_users – Top user registrations
9) top_ins – Top insurance transactions

**📊 Streamlit Dashboard Features
🔹 Global Filters**
1) Year selector
2) Quarter selector

**💳 Transactions Tab**
1) State-wise transaction value & count (India map)
2) Category-wise transaction analysis
3) Top states, districts, and pincodes
4) Year-wise growth trends

**👥 Users Tab**
1) Registered users by state (map)
2) App opens vs registrations
3) Top states, districts, pincodes
4) Engagement ratio analysis

**🛡 Insurance Tab**
1) State-wise insurance policies & premium
2) District & pincode-level insights
3) Insurance adoption trends over years

**📈 Business Case Studies**
The project includes 5 detailed business analyses:

**1️⃣ Device Dominance & User Engagement**
1) Android vs iOS dominance
2) Brand-wise transaction trends
3) Engagement ratio by state

**2️⃣ User Engagement & Growth Strategy**
1) Registration vs app opens
2) Growth trends over years
3) High-potential states & districts

**3️⃣ Transaction Analysis (State & District)**
1) High-value transaction regions
2) Top contributing districts & pincodes
3) Year-wise transaction growth

**4️⃣ User Registration Analysis**
1) Registration hotspots
2) Urban vs emerging regions
3) Registration vs engagement gap

5️⃣ Insurance Transactions Analysis
1) Insurance adoption by geography
2) Premium growth trends
3) High-potential underpenetrated regions

Each case study includes visual insights + business recommendations.














