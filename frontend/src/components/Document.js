


import React, { useState } from 'react';
import DocumentStatus from './DocumentStatus';
import DocumentVersionUpload from './DocumentVersionUpload';
import DocumentVersions from './DocumentVersions';

const Document = ({ document }) => {
  const [status, setStatus] = useState(document.status);

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '5px' }}>
      <h3>{document.title}</h3>
      <p><strong>Document Number:</strong> {document.document_number}</p>
      <p><strong>Status:</strong> {status}</p>
      {document.description && (
        <p><strong>Description:</strong> {document.description}</p>
      )}
      <DocumentVersionUpload documentId={document.id} />
      <DocumentVersions documentId={document.id} />
      <DocumentStatus documentId={document.id} status={status} onStatusChange={setStatus} />
    </div>
  );
};

export default Document;


