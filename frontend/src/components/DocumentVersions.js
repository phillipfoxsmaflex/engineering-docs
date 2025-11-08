




import React, { useState, useEffect } from 'react';
import api from '../api';

const DocumentVersions = ({ documentId }) => {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (documentId) {
      api.get(`/document-versions/document/${documentId}`)
        .then(response => {
          setVersions(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching document versions:", error);
          setLoading(false);
        });
    }
  }, [documentId]);

  return (
    <div>
      <h3>Document Versions</h3>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {versions.map(version => (
            <li key={version.id}>
              Version: {version.version_number} - Uploaded at: {new Date(version.uploaded_at).toLocaleString()}
              {version.comment && <p>Comment: {version.comment}</p>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DocumentVersions;




