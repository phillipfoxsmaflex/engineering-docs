




import React, { useState, useEffect } from 'react';
import api from '../api';

const DocumentVersions = ({ documentId }) => {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVersion1, setSelectedVersion1] = useState(null);
  const [selectedVersion2, setSelectedVersion2] = useState(null);

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

  const handleDownload = (filePath) => {
    // Create a temporary link element and trigger download
    const link = document.createElement('a');
    link.href = `${process.env.REACT_APP_API_BASE_URL}/${filePath}`;
    link.download = filePath.substring(filePath.lastIndexOf('/') + 1);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCompare = () => {
    if (!selectedVersion1 || !selectedVersion2) {
      alert('Please select two versions to compare');
      return;
    }

    // For simplicity, we'll just open both files in new tabs
    // In a real-world application, you might want to implement a diff viewer
    window.open(`${process.env.REACT_APP_API_BASE_URL}/${selectedVersion1.file_path}`, '_blank');
    window.open(`${process.env.REACT_APP_API_BASE_URL}/${selectedVersion2.file_path}`, '_blank');
  };

  return (
    <div>
      <h3>Document Versions</h3>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <ul>
            {versions.map(version => (
              <li key={version.id}>
                Version: {version.version_number} - Uploaded at: {new Date(version.uploaded_at).toLocaleString()}
                {version.comment && <p>Comment: {version.comment}</p>}
                <button onClick={() => handleDownload(version.file_path)}>Download</button>
                {[selectedVersion1, selectedVersion2].includes(version) ?
                  <button onClick={() => {
                    if (version.id === selectedVersion1?.id) {
                      setSelectedVersion1(null);
                    } else {
                      setSelectedVersion2(null);
                    }
                  }}>
                    Deselect
                  </button> :
                  <button onClick={() => {
                    if (!selectedVersion1) {
                      setSelectedVersion1(version);
                    } else if (!selectedVersion2 && version.id !== selectedVersion1.id) {
                      setSelectedVersion2(version);
                    }
                  }}>
                    Select for comparison
                  </button>
                }
              </li>
            ))}
          </ul>
          {selectedVersion1 && selectedVersion2 && (
            <div>
              <h4>Compare Versions</h4>
              <p>Version 1: {selectedVersion1.version_number}</p>
              <p>Version 2: {selectedVersion2.version_number}</p>
              <button onClick={handleCompare}>Compare</button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default DocumentVersions;




