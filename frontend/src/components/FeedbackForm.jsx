import { useEffect, useState } from "react";

function FeedbackForm() {
  const [question, setQuestion] = useState("");
  const [feedback, setFeedback] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch a random question on load
  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    try {
      const res = await fetch("http://localhost:5000/question");
      const data = await res.json();
      setQuestion(data.question);
    } catch (err) {
      setQuestion("Unable to load question.");
    }
  };

  const submitFeedback = async () => {
    if (!feedback.trim()) {
      setMessage("Please enter your feedback.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          feedback
        })
      });

      if (res.ok) {
        setMessage("Feedback saved successfully.");
        setFeedback("");
        fetchQuestion(); // load next random question
      } else {
        setMessage("Something went wrong. Please try again.");
      }
    } catch (err) {
      setMessage("Server error. Please try later.");
    }

    setLoading(false);
  };

  return (
    <div>
      <p><strong>{question}</strong></p>

      <textarea
        rows="4"
        placeholder="Your opinion..."
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        disabled={loading}
        style={{ width: "100%", padding: "10px" }}
      />

      <br /><br />

      <button onClick={submitFeedback} disabled={loading}>
        {loading ? "Submitting..." : "Submit"}
      </button>

      {message && <p>{message}</p>}
    </div>
  );
}

export default FeedbackForm;
