import React from 'react';
import Navbar from './Navbar';
import ContractUploader from './ContractUploader';
import QnADisplay from './QnADisplay';

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Navbar />
      <div className="flex-grow container mx-auto px-4 py-8">
        <ContractUploader />
        <QnADisplay />
      </div>
    </div>
  );
}

export default App;
