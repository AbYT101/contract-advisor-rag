import React, { useState } from 'react';
import api from '../services/api';

function ContractUploader() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.uploadFile(formData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Failed to upload file');
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow-md">
      <h2 className="text-xl mb-4">Upload Contract</h2>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-600 text-white py-2 px-4 rounded">Upload</button>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
}

export default ContractUploader;
