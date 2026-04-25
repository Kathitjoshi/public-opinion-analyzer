# 📊 Public Opinion Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![React 18.x](https://img.shields.io/badge/React-18.x-61DAFB.svg)](https://reactjs.org/)
[![Flask 3.0.0](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)

**Public Opinion Analyzer** is a full-stack web application designed to collect and analyze public opinions on contemporary social, environmental, and policy-related questions. The system leverages transformer-based natural language processing (NLP) models to perform sentiment analysis and text summarization while maintaining a clean and unbiased user experience.

🚀 **[Try Live Demo on HuggingFace Space](https://huggingface.co/spaces/Kathit/public-opinion-analyzer)**

> [!NOTE]
> The HuggingFace Space uses a simplified Gradio-based interface for quick deployment. Run the project locally to access the full **React + Flask** architecture with advanced features and API endpoints.

---

## ✨ Features

* **Randomized Questions**: Opinion-based questions selected randomly using sampling with replacement.
* **Real-time Sentiment Analysis**: Powered by the **DistilBERT** transformer model.
* **Abstractive Summarization**: Generates concise, meaningful summaries using **DistilBART**.
* **Duplicate Detection**: Cryptographic hashing (SHA-256) prevents duplicate submissions and spam.
* **Timestamped Storage**: All feedback is stored with ISO 8601 timestamps for chronological tracking.
* **CSV Persistence**: Fault-tolerant, human-readable data storage (no database setup required).
* **RESTful API**: Clean separation between frontend UI and backend logic.
* **Live Analytics**: Real-time sentiment distribution statistics and percentages.

---

## 🛠 Tech Stack

### Frontend
* **React 18.x** - Component-based UI logic.
* **JavaScript (ES6+)** - Modern frontend syntax.
* **CSS3** - Responsive styling and layout.
* **Fetch API** - Asynchronous HTTP requests.

### Backend
* **Python 3.10+** - Core language for NLP and API logic.
* **Flask 3.0.0** - Lightweight web framework.
* **Flask-CORS** - Cross-origin resource sharing support.

### NLP Models
* **Sentiment Analysis**: `distilbert-base-uncased-finetuned-sst-2-english`
    * *Accuracy*: ~91-92% (SST-2 benchmark).
    * *Logic*: Binary classification with a custom neutral threshold.
* **Summarization**: `sshleifer/distilbart-cnn-12-6`
    * *Type*: Abstractive text generation.
    * *Constraint*: Max length of 60 tokens.

---

## 🏗 System Architecture

### How It Works
1.  **Frontend**: Requests a random opinion question from the `/api/question` endpoint.
2.  **User**: Submits textual feedback through the React-based interface.
3.  **Backend**: Processes the submission through the following pipeline:
    * **Validation**: Checks for minimum input length (10 characters).
    * **Deduplication**: Generates a SHA-256 hash to ensure the entry is unique.
    * **Sentiment**: Classifies text as **POSITIVE**, **NEGATIVE**, or **NEUTRAL**.
    * **Summary**: Creates an abstractive summary via a seq2seq model.
    * **Storage**: Appends the entry to the CSV file with a UTC timestamp.
4.  **Response**: Returns success confirmation and analyzed data to the user.
5.  **Analytics**: Distribution data is calculated on-the-fly via the `/api/stats` endpoint.

---

## 🔌 API Endpoints (add it to backend url end)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health check and model status. |
| `GET` | `/api/question` | Returns a random opinion question. |
| `POST` | `/api/submit` | Submit user feedback (Requires `question` and `feedback`). |
| `GET` | `/api/results` | Retrieve all stored feedback entries (JSON). |
| `GET` | `/api/stats` | Get sentiment distribution statistics and percentages. |

---

## 📂 Data Storage

### CSV Schema
Feedback is stored in `backend/data/feedback.csv` with the following structure:

| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp` | ISO 8601 | Submission time (UTC). |
| `question` | string | The question asked of the user. |
| `feedback` | string | User's raw textual feedback. |
| `summary` | string | AI-generated summary. |
| `sentiment` | enum | POSITIVE, NEGATIVE, or NEUTRAL. |
| `hash` | SHA-256 | Cryptographic hash for deduplication. |

---

## 📂 Folder Structure

```text
public-opinion-analyzer/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── requirements.txt        # Python dependencies
│   └── data/
│       └── feedback.csv        # Auto-generated storage
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── App.jsx            # Main React entry point
|   |   |── index.jsx
│   │   └── App.css             # Styling
│   ├── public/
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
├── .github/
│   └── workflows/              # CI/CD automation
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
* **Node.js** 18.x or higher
* **Python** 3.10 or higher

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*Backend will run at `http://localhost:5000`.*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
*Frontend will run at `http://localhost:3000`.*

---

## 🧠 Sentiment Model Logic

To improve robustness for real-world opinions, we implement a confidence-based threshold for neutrality. If the model's prediction score is below the threshold, it is classified as **NEUTRAL**:

$$\text{if } \text{confidence\_score} < 0.65 \implies \text{Sentiment} = \text{NEUTRAL}$$

This prevents forcing ambiguous text into binary (Positive/Negative) categories.

---

## 🔧 Troubleshooting

* **CORS Errors**: Ensure the backend is running on port 5000 and that the `API_URL` in `frontend/src/App.jsx` points to `http://localhost:5000/api`.
* **Model Load Time**: On the first run, the system will download approximately 500MB of model weights. Please wait 2-3 minutes. Subsequent starts are near-instant.
* **CSV Missing**: The `data/` directory and `feedback.csv` are created automatically on the first API call.

---

## 🔮 Future Enhancements
- [ ] PostgreSQL database integration for enterprise-level scaling.
- [ ] Interactive visualization dashboards using Chart.js or D3.js.
- [ ] Multi-language support (Translation API integration).
- [ ] Docker containerization for one-click deployment.
- [ ] User authentication and session management.

---

## 📊 Architectural Diagrams

### System Workflow
<img width="1536" height="1024" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/78887998-d166-4a6d-a4c7-0d2fb2989d37" />

### Data Integrity
![Hashing Algorithm](https://github.com/user-attachments/assets/31c5293a-b335-45c5-9c7b-80e2c40621b7)

---

## 📜 License & Contact

**License**: MIT  
**GitHub**: [@Kathitjoshi](https://github.com/Kathitjoshi)  
**HuggingFace Space**: [public-opinion-analyzer](https://huggingface.co/spaces/Kathit/public-opinion-analyzer)

**Built with ❤️ for transparent and unbiased public opinion collection.**