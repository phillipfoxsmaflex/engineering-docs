


import React from 'react';

const Document = ({ document }) => {
  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '5px' }}>
      <h3>{document.title}</h3>
      <p><strong>Document Number:</strong> {document.document_number}</p>
      <p><strong>Status:</strong> {document.status}</p>
      {document.description && (
        <p><strong>Description:</strong> {document.description}</p>
      )}
    </div>
  );
};

export default Document;


