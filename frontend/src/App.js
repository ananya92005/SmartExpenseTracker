import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import Navigation from './components/Navigation';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Expenses from './components/Expenses';
import Analytics from './components/Analytics';
import Profile from './components/Profile';
import { AuthProvider } from './context/AuthContext';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on app load
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="loading-spinner"></div>
        <span className="ms-2">Loading...</span>
      </div>
    );
  }

  return (
    <AuthProvider>
      <Router>
        <div className="app-container">
          <Navigation />
          <Container className="py-4">
            <div className="main-content p-4">
              <Routes>
                <Route
                  path="/"
                  element={
                    isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
                  }
                />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/expenses" element={<Expenses />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </div>
          </Container>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;