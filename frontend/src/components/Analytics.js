import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Alert, Button, Badge } from 'react-bootstrap';
import { FaChartLine, FaRobot, FaLightbulb, FaCalendarAlt } from 'react-icons/fa';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Analytics = () => {
  const [insights, setInsights] = useState(null);
  const [clustering, setClustering] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const [insightsRes, clusteringRes, predictionRes, trendsRes] = await Promise.all([
        axios.get('/analytics/insights/'),
        axios.get('/analytics/clustering/').catch(() => ({ data: null })),
        axios.get('/analytics/prediction/').catch(() => ({ data: null })),
        axios.get('/analytics/spending-trends/')
      ]);

      setInsights(insightsRes.data);
      setClustering(clusteringRes.data);
      setPrediction(predictionRes.data);
      setTrends(trendsRes.data);
    } catch (error) {
      setError('Failed to load analytics data');
      console.error('Analytics error:', error);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchAnalyticsData();
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="loading-spinner"></div>
        <p className="mt-2">Loading analytics...</p>
      </div>
    );
  }

  // Prepare chart data
  const categoryChartData = insights?.category_breakdown ? {
    labels: Object.keys(insights.category_breakdown),
    datasets: [{
      label: 'Amount ($)',
      data: Object.values(insights.category_breakdown),
      backgroundColor: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
      ],
      borderWidth: 1,
    }],
  } : null;

  const trendsChartData = trends?.weekly_spending ? {
    labels: trends.weekly_spending.map(week => week.week),
    datasets: [{
      label: 'Weekly Spending ($)',
      data: trends.weekly_spending.map(week => week.total),
      borderColor: '#667eea',
      backgroundColor: 'rgba(102, 126, 234, 0.1)',
      tension: 0.4,
    }],
  } : null;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>
          <FaChartLine className="me-2" />
          Analytics & Insights
        </h1>
        <Button variant="outline-primary" onClick={refreshData}>
          Refresh Data
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      {/* Insights Cards */}
      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <FaRobot className="me-2" />
              AI Insights
            </Card.Header>
            <Card.Body>
              {insights?.suggestions && insights.suggestions.length > 0 ? (
                <div>
                  {insights.suggestions.map((suggestion, index) => (
                    <div key={index} className="mb-3 p-3 bg-light rounded">
                      <FaLightbulb className="text-warning me-2" />
                      {suggestion}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted">Add more expenses to get AI-powered insights!</p>
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header>
              <FaCalendarAlt className="me-2" />
              Spending Overview
            </Card.Header>
            <Card.Body>
              <Row>
                <Col xs={6}>
                  <h4 className="text-primary">${insights?.total_spending?.toFixed(2) || '0.00'}</h4>
                  <small className="text-muted">Total Spent</small>
                </Col>
                <Col xs={6}>
                  <h4 className="text-success">${insights?.average_expense?.toFixed(2) || '0.00'}</h4>
                  <small className="text-muted">Average</small>
                </Col>
              </Row>
              {insights?.highest_category && (
                <div className="mt-3">
                  <Badge bg="info" className="me-2">Top Category:</Badge>
                  {insights.highest_category} (${insights.highest_category_amount?.toFixed(2)})
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Charts */}
      <Row className="mb-4">
        {categoryChartData && (
          <Col md={6}>
            <Card className="chart-container">
              <Card.Header>Category Breakdown</Card.Header>
              <Card.Body>
                <Doughnut
                  data={categoryChartData}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </Card.Body>
            </Card>
          </Col>
        )}

        {trendsChartData && (
          <Col md={6}>
            <Card className="chart-container">
              <Card.Header>Weekly Spending Trends</Card.Header>
              <Card.Body>
                <Line
                  data={trendsChartData}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        display: false,
                      },
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          callback: function(value) {
                            return '$' + value;
                          }
                        }
                      }
                    }
                  }}
                />
              </Card.Body>
            </Card>
          </Col>
        )}
      </Row>

      {/* ML Features */}
      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              🤖 Machine Learning Clustering
            </Card.Header>
            <Card.Body>
              {clustering ? (
                <div>
                  <p><strong>Status:</strong> <Badge bg="success">Active</Badge></p>
                  <p><strong>Silhouette Score:</strong> {clustering.silhouette_score?.toFixed(3) || 'N/A'}</p>
                  <p className="text-muted small">{clustering.interpretation}</p>
                  <small className="text-muted">
                    Groups your expenses into spending patterns using KMeans algorithm.
                  </small>
                </div>
              ) : (
                <div>
                  <p><strong>Status:</strong> <Badge bg="warning">Need More Data</Badge></p>
                  <p className="text-muted">Add at least 3 expenses to enable clustering analysis.</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>
              🔮 Expense Prediction
            </Card.Header>
            <Card.Body>
              {prediction ? (
                <div>
                  <p><strong>Status:</strong> <Badge bg="success">Active</Badge></p>
                  <p><strong>Next Month:</strong> ${prediction.next_month_prediction?.toFixed(2)}</p>
                  <p><strong>Next Week:</strong> ${prediction.next_week_prediction?.toFixed(2)}</p>
                  <p><strong>Confidence:</strong> {(prediction.confidence * 100)?.toFixed(1)}%</p>
                  <small className="text-muted">
                    Predictions based on your historical spending patterns.
                  </small>
                </div>
              ) : (
                <div>
                  <p><strong>Status:</strong> <Badge bg="warning">Need More Data</Badge></p>
                  <p className="text-muted">Add at least 7 expenses to enable predictions.</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Analytics;