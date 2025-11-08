



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

  const renderStatusOptions = () => {
    switch(status) {
      case 'Entwurf':
        return (
          <>
            <option value="In Prüfung">In Prüfung</option>
          </>
        );
      case 'In Prüfung':
        return (
          <>
            <option value="Genehmigt">Genehmigt</option>
            <option value="Abgelehnt">Abgelehnt</option>
          </>
        );
      case 'Abgelehnt':
        return (
          <>
            <option value="Entwurf">Entwurf</option>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }}>
      <h3>Update Status for Document ID: {documentId}</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label><strong>Current Status:</strong></label>
          <span style={{ marginLeft: '10px', fontWeight: 'bold', color: status === 'Genehmigt' ? 'green' : (status === 'Abgelehnt' ? 'red' : 'orange') }}>
            {status}
          </span>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label><strong>New Status:</strong></label>
          <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)} style={{ marginLeft: '10px' }}>
            <option value="">Select status</option>
            {renderStatusOptions()}
          </select>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label><strong>Comment:</strong></label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows="3"
            style={{ width: '100%', marginLeft: '10px' }}
            placeholder="Enter a comment for this status update"
          ></textarea>
        </div>
        <button type="submit" style={{ marginTop: '10px', padding: '5px 10px' }}>Update Status</button>
      </form>
    </div>
  );
};

export default DocumentStatus;



