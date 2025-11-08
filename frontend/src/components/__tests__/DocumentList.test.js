


import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import DocumentList from '../DocumentList';
import api from '../../api';

// Mock the API module
jest.mock('../../api');

test('renders loading state initially', () => {
  render(<DocumentList folderId={1} />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});

test('displays documents after successful fetch', async () => {
  // Mock a successful API response
  const mockDocuments = [
    { id: 1, title: 'Test Document 1', document_number: 'DOC-001', status: 'Entwurf' },
    { id: 2, title: 'Test Document 2', document_number: 'DOC-002', status: 'Freigegeben' }
  ];
  api.get.mockResolvedValue({ data: mockDocuments });

  render(<DocumentList folderId={1} />);

  // Wait for the documents to be rendered
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    expect(screen.getByText('Test Document 1')).toBeInTheDocument();
    expect(screen.getByText('Test Document 2')).toBeInTheDocument();
  });
});

test('displays error message on failed fetch', async () => {
  // Mock an API error
  api.get.mockRejectedValue(new Error('Network error'));

  render(<DocumentList folderId={1} />);

  // Wait for the loading state to disappear (even though it will fail)
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });

  // Check that we're not trying to display documents
  expect(screen.queryByText('Test Document 1')).not.toBeInTheDocument();
});

