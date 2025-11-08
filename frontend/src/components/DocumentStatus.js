



import React, { useState } from 'react';
import api from '../api';

const DocumentStatus = ({ documentId, status, onStatusChange }) => {
  const [newStatus, setNewStatus] = useState('');
  const [comment, setComment] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.put(`/document-status/${documentId}`, {
        status: newStatus,
        comment
      });
      onStatusChange(newStatus);
      alert('Document status updated successfully!');
    } catch (error) {
      console.error("Error updating document status:", error);
      alert('Failed to update document status');
    }
  };

  return (
    <div>
      <h3>Update Status for: {documentId}</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>New Status:</label>
          <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
            <option value="">Select status</option>
            {status === 'Entwurf' && (
              <>
                <option value="In Prüfung">In Prüfung</option>
              </>
            )}
            {status === 'In Prüfung' && (
              <>
                <option value="Genehmigt">Genehmigt</option>
                <option value="Abgelehnt">Abgelehnt</option>
              </>
            )}
            {status === 'Abgelehnt' && (
              <>
                <option value="Entwurf">Entwurf</option>
              </>
            )}
          </select>
        </div>
        <div>
          <label>Comment:</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          ></textarea>
        </div>
        <button type="submit">Update Status</button>
      </form>
    </div>
  );
};

export default DocumentStatus;



