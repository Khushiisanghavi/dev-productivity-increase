# 🚀 Developer Productivity Dashboard

## 📌 Overview

Engineering teams generate a large amount of data—pull requests, deployments, and bug reports—but this data is often difficult to interpret and act upon.

This project is a lightweight **Developer Productivity Dashboard** that transforms raw engineering data into **meaningful insights and actionable recommendations**.

Instead of just displaying metrics, the system helps users understand:
- What is happening
- Why it is happening
- What actions to take

---

## 🎯 Problem Statement

Developers and teams often track metrics like cycle time or lead time, but these numbers alone do not provide clear direction.

The goal of this project is to:
> Convert engineering data into insights that improve development speed, efficiency, and code quality.

---

## 🧠 Key Features

### 📊 Metrics Tracked
- **Lead Time** – Time from PR creation to deployment  
- **Cycle Time** – Time from PR creation to merge  
- **Deployment Frequency** – Number of deployments per day  
- **Bug Rate** – Bugs per PR  

---

### 📈 Trend Analysis
- Visualizes how metrics change over time  
- Helps detect performance degradation or improvement  

---

### 📉 Change Detection
- Calculates percentage change in key metrics  
- Highlights significant increases or decreases  

---

### 🏥 System Health Score
- Aggregates multiple metrics into a single score  
- Provides a quick overview of system performance  

---

### 🧠 Insight Generation (Core Feature)
- Interprets metrics instead of just displaying them  
- Identifies issues such as:
  - Increasing cycle time  
  - Rising bug rate  
- Suggests actionable improvements  

---

### 🎛️ Interactive Dashboard
- Filter data based on recent activity  
- Dynamically updates metrics and trends  

---

## 🏗️ Architecture
project/
│
├── backend/
│ └── main.py
│
├── frontend/
│ └── app.py
│
├── data/
│ └── mock_data.json
│
└── README.md

---

## ⚙️ Setup & Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn streamlit requests pandas

cd backend
uvicorn main:app --reload

cd frontend
streamlit run app.py

```