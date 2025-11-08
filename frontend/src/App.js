import React, { useState } from 'react';
import './App.css';
import './components/styles.css';
import FolderBrowser from './components/FolderBrowser';
import DocumentList from './components/DocumentList';
import DocumentUpload from './components/DocumentUpload';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [selectedFolderId, setSelectedFolderId] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App container">
      <header className="header">
        <h1>Engineering Document Management System</h1>
        <button className="button button-primary" onClick={() => setShowDashboard(!showDashboard)}>
          {showDashboard ? 'Hide Dashboard' : 'Show Dashboard'}
        </button>
      </header>
      <main style={{ display: 'flex' }}>
        {!showDashboard && (
          <>
            <aside style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px' }}>
              <FolderBrowser onSelect={setSelectedFolderId} />
            </aside>
            <section style={{ flexGrow: 1, padding: '10px' }}>
              {selectedFolderId && <DocumentUpload folderId={selectedFolderId} />}
              <DocumentList folderId={selectedFolderId} />
            </section>
          </>
        )}
        {showDashboard && (
          <div style={{ width: '100%', padding: '10px' }}>
            <Dashboard />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
