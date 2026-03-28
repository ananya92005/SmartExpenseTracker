import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Alert, Button } from 'react-bootstrap';
import { FaPlus, FaWallet, FaChartLine, FaLightbulb } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import axios from '../services/api';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryResponse, insightsResponse] = await Promise.all([
        axios.get('/expenses/summary/'),
        axios.get('/analytics/insights/')
      ]);

      setSummary(summaryResponse.data);
      setInsights(insightsResponse.data);
    } catch (error) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="loading-spinner"></div>
        <p className="mt-2">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="mb-4">Dashboard</h1>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row className="mb-4">
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaWallet size={30} className="text-primary mb-2" />
              <h4>${summary?.total?.toFixed(2) || '0.00'}</h4>
              <p className="text-muted">Total Expenses</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaChartLine size={30} className="text-success mb-2" />
              <h4>{summary?.count || 0}</h4>
              <p className="text-muted">Total Transactions</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaLightbulb size={30} className="text-warning mb-2" />
              <h4>${summary?.average?.toFixed(2) || '0.00'}</h4>
              <p className="text-muted">Average Expense</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <Link to="/expenses">
                <Button variant="primary" className="w-100">
                  <FaPlus className="me-2" />
                  Add Expense
                </Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {insights && (
        <Row>
          <Col md={6}>
            <Card>
              <Card.Header>
                <h5>Top Spending Category</h5>
              </Card.Header>
              <Card.Body>
                <h3 className="text-primary">
                  {insights.highest_category || 'No expenses yet'}
                </h3>
                {insights.highest_category && (
                  <p className="text-muted">
                    ${insights.highest_category_amount?.toFixed(2)} spent
                  </p>
                )}
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card>
              <Card.Header>
                <h5>Smart Suggestions</h5>
              </Card.Header>
              <Card.Body>
                {insights.suggestions && insights.suggestions.length > 0 ? (
                  <ul className="list-unstyled">
                    {insights.suggestions.map((suggestion, index) => (
                      <li key={index} className="mb-2">
                        💡 {suggestion}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-muted">Add more expenses to get personalized suggestions!</p>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      <Row className="mt-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>Quick Actions</h5>
            </Card.Header>
            <Card.Body>
              <div className="d-grid gap-2">
                <Link to="/expenses" className="btn btn-outline-primary">
                  <FaWallet className="me-2" />
                  Manage Expenses
                </Link>
                <Link to="/analytics" className="btn btn-outline-success">
                  <FaChartLine className="me-2" />
                  View Analytics
                </Link>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>Recent Activity</h5>
            </Card.Header>
            <Card.Body>
              {summary?.count > 0 ? (
                <p>You have {summary.count} expense{summary.count !== 1 ? 's' : ''} recorded.</p>
              ) : (
                <div className="text-center">
                  <p className="text-muted mb-3">No expenses recorded yet.</p>
                  <Link to="/expenses" className="btn btn-primary">
                    <FaPlus className="me-2" />
                    Add Your First Expense
                  </Link>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;