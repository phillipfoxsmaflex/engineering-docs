import React, { useState } from 'react';
import './App.css';
import FolderBrowser from './components/FolderBrowser';
import DocumentList from './components/DocumentList';
import DocumentUpload from './components/DocumentUpload';
import Login from './components/Login';

function App() {
  const [selectedFolderId, setSelectedFolderId] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Engineering Document Management System</h1>
      </header>
      <main style={{ display: 'flex' }}>
        <aside style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px' }}>
          <FolderBrowser onSelect={setSelectedFolderId} />
        </aside>
        <section style={{ flexGrow: 1, padding: '10px' }}>
          {selectedFolderId && <DocumentUpload folderId={selectedFolderId} />}
          <DocumentList folderId={selectedFolderId} />
        </section>
      </main>
    </div>
  );
}

export default App;
