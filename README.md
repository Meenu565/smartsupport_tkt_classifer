# 🤖 Smart Support Ticket Classifier

## 📌 Overview

The **Smart Support Ticket Classifier** is an AI-powered system designed to automatically classify customer support messages and assign priority levels. It helps reduce manual effort, improves response time, and provides actionable insights through an interactive dashboard.

The system supports both:

* ✅ **Real-time classification (Streamlit UI)**
* ✅ **Batch processing (JSON output for multiple messages)**

---

## 🎯 Problem Statement

Customer support teams receive a high volume of messages daily. These messages vary in type and urgency, making manual processing inefficient and error-prone.

This project automates:

* Ticket classification
* Priority assignment
* Data analysis and visualization

---

## 🚀 Features

* 🤖 AI-powered classification using **OpenAI API**
* ⚡ Fast fallback using **Groq API**
* 🛡️ Rule-based fallback for reliability
* 📊 Interactive dashboard (Streamlit)
* 📁 CSV upload + manual ticket entry
* 🔍 Global and tab-level filters
* 📈 Visual analytics (Category, Priority, Time)
* ⬇️ Download filtered data
* 📦 Batch processing with JSON output

---

## 🧠 Categories & Priority

### Categories:

* Billing
* Technical Issue
* Account
* General Inquiry

### Priority Levels:

* High → urgent / blocking issues
* Medium → moderate issues
* Low → general queries

---

## 🧩 Tech Stack

* Python
* OpenAI API
* Groq API
* Streamlit
* Pandas
* Matplotlib

---

## 📂 Project Structure

```
Smart-Support-Ticket-Classifier/
│
├── app.py                  # Streamlit dashboard
├── classifier.py           # AI + rule-based classification
├── utils.py                # Helper functions
├── batch_processor.py      # Batch message processing
├── test.py                 # Sample test script
├── data/
│   └── tickets.csv         # Stored ticket data
├── images/                 # Screenshots
├── .env.example            # Sample environment file
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Smart-Support-Ticket-Classifier.git
cd Smart-Support-Ticket-Classifier
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Create `.env` file

```env
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

⚠️ Do NOT upload `.env` to GitHub

---

### 4️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

### 5️⃣ Run Batch Processing

```bash
python test.py
```

---

## 📊 Sample Output (JSON)

```json
[
  {
    "message": "My payment got deducted but service is not activated",
    "category": "Billing",
    "priority": "High"
  },
  {
    "message": "App crashes every time I login",
    "category": "Technical Issue",
    "priority": "High"
  },
  {
    "message": "How to change my email address?",
    "category": "Account",
    "priority": "Low"
  }
]
```

---

## 📸 Output Screenshots

### Dashboard

![Dashboard](images/dashboard.png)

### Classification Result

![Classification](images/classification.png)

### Charts

![Charts](images/charts.png)

### JSON Output

![Output](images/output.png)

---

## 🧠 Approach

* Used **prompt engineering** for structured JSON output
* Implemented **hybrid classification architecture**:

  * OpenAI (primary)
  * Groq (fallback)
  * Rule-based (failsafe)
* Built **interactive analytics dashboard**
* Ensured **error handling and robustness**

---

## 🔐 Security

* API keys stored securely using `.env`
* `.env` excluded via `.gitignore`
* No sensitive data exposed in repository

---

## 🚀 Future Enhancements

* Ticket status tracking (Open / Closed)
* Sentiment analysis
* Auto-assignment to teams
* Advanced analytics dashboard
* Real-time notifications

---

## 🏁 Conclusion

This project demonstrates how AI can be applied to automate customer support workflows, improve efficiency, and provide meaningful insights through data visualization.

---

## 💬 Author

**Indhu Meenaakshi Anand**

---
