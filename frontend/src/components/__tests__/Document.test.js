


import React from 'react';
import { render, screen } from '@testing-library/react';
import Document from '../Document';

test('renders document title', () => {
  const document = {
    id: 1,
    title: 'Test Document',
    document_number: 'DOC-12345',
    status: 'Entwurf',
    description: 'A test document'
  };

  render(<Document document={document} />);

  expect(screen.getByText('Test Document')).toBeInTheDocument();
  expect(screen.getByText('Document Number: DOC-12345')).toBeInTheDocument();
  expect(screen.getByText('Status: Entwurf')).toBeInTheDocument();
  expect(screen.getByText('Description: A test document')).toBeInTheDocument();
});

test('renders without description if not provided', () => {
  const document = {
    id: 1,
    title: 'Test Document',
    document_number: 'DOC-12345',
    status: 'Entwurf'
    // No description
  };

  render(<Document document={document} />);

  expect(screen.queryByText(/Description:/)).not.toBeInTheDocument();
});


