import { useState } from "react";
import FeedbackForm from "./components/FeedbackForm";
import Dashboard from "./components/Dashboard";
import "./App.css";

function App() {
  const [analytics, setAnalytics] = useState({});

  const isAdmin = window.location.pathname === "/admin";

  if (isAdmin) {
    return <Admin />;
  }

  return (
    <div className="container">
      <h2>Public Opinion Analyzer</h2>
      <FeedbackForm onAnalyticsUpdate={setAnalytics} />
      <hr />
      <Dashboard data={analytics} />
    </div>
  );
}

export default App;
