


import React, { useState, useEffect } from 'react';
import api from '../api';
import Folder from './Folder';

const FolderBrowser = ({ onSelect }) => {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/folders')
      .then(response => {
        setFolders(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching folders:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2>Folder Browser</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        folders.map(folder => (
          <Folder
            key={folder.id}
            folderId={folder.id}
            name={folder.name}
            onSelect={onSelect}
          />
        ))
      )}
    </div>
  );
};

export default FolderBrowser;


