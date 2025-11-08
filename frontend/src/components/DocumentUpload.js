


import React, { useState } from 'react';
import './styles.css';
import api from '../api';

const DocumentUpload = ({ folderId }) => {
  const [title, setTitle] = useState('');
  const [documentNumber, setDocumentNumber] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('document_number', documentNumber);
    formData.append('description', description);
    formData.append('folder_id', folderId || '');
    formData.append('file', file);

    try {
      await api.post('/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Document uploaded successfully!');
      setTitle('');
      setDocumentNumber('');
      setDescription('');
      setFile(null);
    } catch (error) {
      console.error("Error uploading document:", error);
      alert('Failed to upload document');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Upload Document</h2>
      <form className="form-group" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title:</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="documentNumber">Document Number:</label>
          <input
            id="documentNumber"
            type="text"
            value={documentNumber}
            onChange={(e) => setDocumentNumber(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="file">File:</label>
          <input
            id="file"
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </div>
        <button className="button button-primary" type="submit" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
};

export default DocumentUpload;


