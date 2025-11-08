



import React, { useState, useEffect } from 'react';
import api from '../api';
import Document from './Document';

const DocumentList = ({ folderId }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (folderId) {
      api.get(`/documents?folder_id=${folderId}`)
        .then(response => {
          setDocuments(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching documents:", error);
          setLoading(false);
        });
    }
  }, [folderId]);

  return (
    <div>
      <h2>Documents</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        documents.map(document => (
          <Document key={document.id} document={document} />
        ))
      )}
    </div>
  );
};

export default DocumentList;



