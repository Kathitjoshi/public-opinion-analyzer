from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import csv
import os
import hashlib
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# ============================================================
# CONFIGURATION
# ============================================================
CSV_FILE = "data/feedback.csv"
CSV_HEADERS = ["timestamp", "question", "feedback", "summary", "sentiment", "hash"]

QUESTIONS = [
    "What is your opinion on digital surveillance?",
    "Should social media be regulated by the government?",
    "What are your thoughts on remote work culture?",
    "How do you feel about electric vehicles replacing traditional cars?",
    "What is your stance on universal basic income?",
    "Should artificial intelligence be regulated?",
    "What is your opinion on renewable energy adoption?",
    "How do you view the gig economy?",
    "What are your thoughts on data privacy laws?"
]

# ============================================================
# MODEL LOADING
# ============================================================
print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")

print("Loading sentiment analysis model...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1
)
print("✓ Sentiment model loaded\n")

print("Loading summarization model...")
try:
    summarizer_pipeline = pipeline(
        "text2text-generation",
        model="sshleifer/distilbart-cnn-12-6",
        device=-1
    )
    print("✓ Summarizer model loaded (distilbart-cnn-12-6)\n")
except Exception as e:
    print(f"⚠ Primary model failed: {e}")
    print("Loading fallback model...")
    summarizer_pipeline = pipeline(
        "text2text-generation",
        model="facebook/bart-large-cnn",
        device=-1
    )
    print("✓ Summarizer model loaded (facebook/bart-large-cnn)\n")

# ============================================================
# CSV UTILITIES
# ============================================================
def ensure_csv_exists():
    os.makedirs(os.path.dirname(CSV_FILE) if os.path.dirname(CSV_FILE) else "data", exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"✓ Created new CSV file: {CSV_FILE}")

def hash_feedback(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def is_duplicate(feedback_hash):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('hash') == feedback_hash:
                return True
    return False

# ============================================================
# NLP PROCESSING
# ============================================================
def analyze_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    label = result['label']
    score = result['score']
    if score < 0.65:
        label = "NEUTRAL"
    return {"label": label, "score": round(score, 4)}

def generate_summary(text, max_length=60):
    if len(text.split()) < 10:
        return text
    try:
        input_text = f"summarize: {text}"
        result = summarizer_pipeline(
            input_text,
            max_length=max_length,
            min_length=10,
            do_sample=False,
            truncation=True
        )[0]
        return result['generated_text']
    except Exception as e:
        print(f"⚠ Summarization error: {e}")
        words = text.split()
        return ' '.join(words[:30]) + ('...' if len(words) > 30 else '')

# ============================================================
# API ROUTES
# ============================================================
@app.route('/')
def home():
    return jsonify({
        "service": "Public Opinion Analyzer API",
        "status": "running",
        "mode": "local_development",
        "endpoints": {
            "health": "/api/health",
            "get_question": "/api/question",
            "submit_feedback": "/api/submit",
            "view_results": "/api/results",
            "view_stats": "/api/stats"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "csv_exists": os.path.exists(CSV_FILE),
        "csv_path": os.path.abspath(CSV_FILE),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/question', methods=['GET'])
def get_question():
    question = random.choice(QUESTIONS)
    return jsonify({"question": question})

@app.route('/api/submit', methods=['POST'])
def submit_feedback():
    ensure_csv_exists()
    
    data = request.json
    question = data.get('question', '')
    feedback = data.get('feedback', '')
    
    if not feedback or len(feedback.strip()) < 10:
        return jsonify({"error": "Feedback must be at least 10 characters"}), 400
    
    feedback_hash = hash_feedback(feedback)
    if is_duplicate(feedback_hash):
        return jsonify({"error": "Duplicate feedback detected"}), 409
    
    print(f"Processing feedback: {feedback[:50]}...")
    sentiment_result = analyze_sentiment(feedback)
    summary = generate_summary(feedback)
    
    timestamp = datetime.now().isoformat()
    row = [timestamp, question, feedback, summary, sentiment_result['label'], feedback_hash]
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    print(f"✓ Stored feedback | Sentiment: {sentiment_result['label']}")
    print(f"✓ CSV location: {os.path.abspath(CSV_FILE)}")
    
    return jsonify({
        "status": "success",
        "message": "Thank you for your feedback!",
        "sentiment": sentiment_result['label'],
        "summary": summary
    })

@app.route('/api/results', methods=['GET'])
def get_results():
    if not os.path.exists(CSV_FILE):
        return jsonify({"total": 0, "data": []})
    
    results = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    return jsonify({
        "total": len(results),
        "data": results
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if not os.path.exists(CSV_FILE):
        return jsonify({
            "total_responses": 0,
            "sentiment_breakdown": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0},
            "percentages": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        })
    
    sentiments = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    total = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sentiment = row.get('sentiment', 'NEUTRAL')
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
            total += 1
    
    return jsonify({
        "total_responses": total,
        "sentiment_breakdown": sentiments,
        "percentages": {
            k: round((v/total)*100, 2) if total > 0 else 0 
            for k, v in sentiments.items()
        }
    })

# ============================================================
# STARTUP
# ============================================================
if __name__ == '__main__':
    ensure_csv_exists()
    print("=" * 60)
    print("🚀 Public Opinion Analyzer Backend Running")
    print("   Local Development Mode")
    print("   Backend: http://localhost:5000")
    print("   Frontend: http://localhost:3000")
    print(f"   Data storage: {os.path.abspath(CSV_FILE)}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)