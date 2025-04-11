import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ResumeMatcher from './pages/ResumeMatcher.js';
import EmotionCheck from './pages/EmotionCheck.js';
import BookInterview from './pages/BookInterview.js';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/resume-matcher">Resume Matcher</Link></li>
            <li><Link to="/emotion-check">Emotion Check</Link></li>
            <li><Link to="/book-interview">Book Interview</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<div>Welcome to AI Interview Platform</div>} />
          <Route path="/resume-matcher" element={<ResumeMatcher />} />
          <Route path="/emotion-check" element={<EmotionCheck />} />
          <Route path="/book-interview" element={<BookInterview />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;