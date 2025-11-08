




import React, { useState } from 'react';
import api from '../api';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post('/auth/token', {
        username,
        password
      });
      localStorage.setItem('token', response.data.access_token);
      onLogin();
    } catch (error) {
      console.error("Error logging in:", error);
      alert('Failed to login');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <p>For first-time setup, use the default admin credentials:</p>
      <ul>
        <li><strong>Username:</strong> admin</li>
        <li><strong>Password:</strong> password123</li>
      </ul>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;




