# Public Opinion Analyzer

Public Opinion Analyzer is a full-stack web application designed to collect and analyze public opinions on contemporary social, environmental, and policy-related questions. The system leverages transformer-based natural language processing models to perform sentiment analysis and text summarization while maintaining a clean and unbiased user experience.

The project focuses on simplicity, reliability, and interview-ready system design rather than overengineering.

---

## Features

- Randomized opinion-based questions (sampling with replacement)
- User feedback collection through a web interface
- Transformer-based sentiment analysis
- Abstractive text summarization
- Duplicate feedback detection using cryptographic hashing
- Timestamped feedback storage
- Fault-tolerant CSV-based persistence
- Clear separation between frontend and backend logic

---

## Tech Stack

### Frontend
- React
- JavaScript
- HTML
- CSS

### Backend
- Python
- Flask

### Natural Language Processing
- HuggingFace Transformers
- Sentiment Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Summarization Model: `sshleifer/distilbart-cnn-12-6`

---

## How the System Works

1. The frontend requests a random opinion-based question from the backend.
2. The user submits textual feedback.
3. The backend processes the feedback by:
   - Performing sentiment classification
   - Generating a short abstractive summary
   - Detecting duplicate submissions using hashing
4. The feedback is stored along with metadata.
5. The user receives a simple confirmation message.

All analytical processing is handled on the backend to avoid bias and keep the user interface minimal.

---

## Sentiment Model Accuracy

The sentiment analysis component is based on DistilBERT fine-tuned on the Stanford Sentiment Treebank (SST-2) dataset.

- Benchmark accuracy: approximately 91–92%
- Task: Binary sentiment classification (Positive / Negative)

A confidence-based threshold is used to classify uncertain predictions as Neutral, improving robustness for real-world, opinion-based inputs.

Actual accuracy may vary depending on domain-specific language.

---

## Data Storage

Feedback is stored in a CSV file with the following fields:
- timestamp
- question
- feedback
- summary
- sentiment
- hash

Key characteristics of the storage design:
- Automatic file creation and repair
- Protection against duplicate submissions
- Human-readable and transparent format

---

## Folder Structure
```
public-opinion-analyzer/
├── backend/
│   ├── app.py
│   ├── ml/
│   │   └── sentiment_model.py
│   ├── nlp/
│   │   └── summarizer.py
│   ├── security/
│   │   └── hash_utils.py
│   └── data/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── public/
│   └── package.json
├── .gitignore
└── README.md
```

---

## Running the Project Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

The application will be accessible at `http://localhost:3000`.

---

## Design Considerations

- Transformer models were chosen to reliably handle opinion-based language.
- Analytics and processing are kept backend-only to avoid influencing users.
- CSV storage was selected for simplicity, transparency, and ease of debugging.
- The modular structure allows easy future enhancements.

---

## Future Enhancements

- Database integration
- Visualization dashboards
- CI/CD automation
- Cloud deployment
- Advanced analytics

---

## License

MIT License