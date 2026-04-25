import { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [question, setQuestion] = useState('');
  const [feedback, setFeedback] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch question on component mount
  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    try {
      const response = await fetch(`${API_URL}/question`);
      const data = await response.json();
      setQuestion(data.question);
      setStatus('');
    } catch (error) {
      console.error('Error fetching question:', error);
      setStatus('❌ Unable to load question. Is the backend running?');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (feedback.length < 10) {
      setStatus('❌ Feedback must be at least 10 characters');
      return;
    }

    setLoading(true);
    setStatus('Processing...');

    try {
      const response = await fetch(`${API_URL}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          feedback
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus(`✅ ${data.message}`);
        setFeedback('');
        fetchQuestion(); // Load new question
      } else {
        setStatus(`❌ ${data.error}`);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setStatus('❌ Failed to submit. Is the backend running on port 5000?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>🗣️ Public Opinion Analyzer</h1>
        <p className="subtitle">Share your thoughts on important topics</p>

        <div className="question-box">
          <h2>{question || 'Loading question...'}</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Your opinion..."
            rows="6"
            disabled={loading}
          />

          <div className="button-group">
            <button 
              type="submit" 
              className="btn-primary"
              disabled={loading || !question}
            >
              {loading ? 'Submitting...' : 'Submit'}
            </button>
            <button 
              type="button" 
              className="btn-secondary"
              onClick={fetchQuestion}
              disabled={loading}
            >
              🔄 New Question
            </button>
          </div>
        </form>

        {status && (
          <div className={`status ${status.includes('✅') ? 'success' : 'error'}`}>
            {status}
          </div>
        )}

        <div className="footer">
          <p>Thx for your time!!</p>
        </div>
      </div>
    </div>
  );
}

export default App;