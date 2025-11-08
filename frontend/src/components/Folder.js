

import React, { useState, useEffect } from 'react';
import './styles.css';
import api from '../api';

const Folder = ({ folderId, name, onSelect }) => {
  const [expanded, setExpanded] = useState(false);
  const [subfolders, setSubfolders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (folderId && expanded) {
      api.get(`/folders/${folderId}/children`)
        .then(response => {
          setSubfolders(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching subfolders:", error);
          setLoading(false);
        });
    }
  }, [folderId, expanded]);

  const handleToggle = () => {
    setExpanded(!expanded);
    if (onSelect && folderId) {
      onSelect(folderId);
    }
  };

  return (
    <div>
      <div
        className="button button-secondary"
        style={{ cursor: 'pointer', marginLeft: '10px' }}
        onClick={handleToggle}
      >
        {expanded ? '▼' : '►'} {name}
      </div>
      {expanded && (
        <div style={{ marginLeft: '20px' }}>
          {loading ? (
            <p>Loading...</p>
          ) : (
            subfolders.map(subfolder => (
              <Folder
                key={subfolder.id}
                folderId={subfolder.id}
                name={subfolder.name}
                onSelect={onSelect}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Folder;

