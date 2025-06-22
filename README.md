# 💳 Real-Time Credit Card Fraud Detection

A complete real-time streaming project to detect credit card fraud using Kafka, PySpark, SQLite, and Streamlit — with a live dashboard and simulated transactions.

---

## 🚀 Tech Stack

| Tool        | Purpose                                 |
|-------------|------------------------------------------|
| **Kafka**   | Real-time messaging / stream transport   |
| **PySpark** | Real-time stream processing              |
| **SQLite**  | Lightweight storage of fraud records     |
| **Streamlit** | Dashboard to visualize fraud in real-time |
| **Faker**   | Generate fake credit card transactions   |

---

## 📌 Features

- 🕵️ Detects fraudulent transactions using simulated logic
- 🔁 Real-time streaming with Kafka
- ⚡ Spark processes and filters only fraud (`is_fraud=1`)
- 💽 Stores fraud into SQLite DB
- 📊 Streamlit dashboard with:
  - Total frauds
  - Table of frauds
  - Bar chart: fraud amount by merchant

---

## 🧠 Project Architecture

```mermaid

