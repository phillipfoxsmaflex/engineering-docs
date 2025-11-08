



import React, { useState } from 'react';
import api from '../api';

const DocumentVersionUpload = ({ documentId }) => {
  const [comment, setComment] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('document_id', documentId);
    formData.append('comment', comment);
    formData.append('file', file);

    try {
      await api.post('/document-versions', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Document version uploaded successfully!');
      setComment('');
      setFile(null);
    } catch (error) {
      console.error("Error uploading document version:", error);
      alert('Failed to upload document version');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Upload New Version for Document ID: {documentId}</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Comment:</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          ></textarea>
        </div>
        <div>
          <label>File:</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
};

export default DocumentVersionUpload;



