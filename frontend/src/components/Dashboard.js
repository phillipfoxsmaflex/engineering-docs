


import React, { useState, useEffect } from 'react';
import './styles.css';
import api from '../api';
import Document from './Document';

const Dashboard = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch documents that are in "In Prüfung" status
    api.get('/documents')
      .then(response => {
        const pendingDocuments = response.data.filter(doc => doc.status === 'In Prüfung');
        setDocuments(pendingDocuments);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching documents:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="container">
      <h2>Dashboard - Documents Pending Review</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        documents.length > 0 ? (
          documents.map(document => (
            <Document key={document.id} document={document} />
          ))
        ) : (
          <p>No documents pending review.</p>
        )
      )}
    </div>
  );
};

export default Dashboard;

