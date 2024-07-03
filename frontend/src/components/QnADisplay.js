
import React, { useState } from 'react';
import api from '../services/api';

function QnADisplay() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleGenerate = async () => {
    if (!question) {
      setResponse('Please enter a question');
      return;
    }

    try {
      const result = await api.generateResponse({ question });
      setResponse(result.data.response);
    } catch (error) {
      setResponse('Failed to get response');
    }
  };

  return (
    <div className="bg-white p-6 mt-6 rounded shadow-md">
      <h2 className="text-xl mb-4">Ask a Question</h2>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full mb-4 p-2 border rounded"
        rows="4"
        placeholder="Enter your question here..."
      />
      <button onClick={handleGenerate} className="bg-blue-600 text-white py-2 px-4 rounded">Ask</button>
      {response && <p className="mt-4 bg-gray-100 p-4 rounded">{response}</p>}
    </div>
  );
}

export default QnADisplay;
