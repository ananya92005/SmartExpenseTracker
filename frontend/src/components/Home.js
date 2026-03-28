import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { FaWallet, FaRobot, FaChartLine, FaShieldAlt } from 'react-icons/fa';

const Home = () => {
  return (
    <Container className="py-5">
      <div className="text-center mb-5">
        <h1 className="display-4 mb-3">
          <FaWallet className="me-3 text-primary" />
          Smart Expense Tracker
        </h1>
        <p className="lead text-muted">
          Take control of your finances with AI-powered expense tracking and insights
        </p>
      </div>

      <Row className="mb-5">
        <Col md={4}>
          <Card className="text-center h-100">
            <Card.Body className="d-flex flex-column">
              <FaWallet size={50} className="text-primary mx-auto mb-3" />
              <h5>Smart Tracking</h5>
              <p className="text-muted flex-grow-1">
                Track your daily expenses with categories, dates, and detailed descriptions.
                Never miss a transaction again.
              </p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center h-100">
            <Card.Body className="d-flex flex-column">
              <FaRobot size={50} className="text-success mx-auto mb-3" />
              <h5>AI Insights</h5>
              <p className="text-muted flex-grow-1">
                Get personalized spending insights and smart suggestions powered by machine learning.
                Understand your spending patterns.
              </p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center h-100">
            <Card.Body className="d-flex flex-column">
              <FaChartLine size={50} className="text-info mx-auto mb-3" />
              <h5>Visual Analytics</h5>
              <p className="text-muted flex-grow-1">
                Beautiful charts and graphs showing your spending trends, category breakdowns,
                and predictive analytics.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-5">
        <Col md={12}>
          <Card className="text-center bg-light">
            <Card.Body>
              <FaShieldAlt size={40} className="text-warning mb-3" />
              <h4>Secure & Private</h4>
              <p className="text-muted mb-0">
                Your financial data is encrypted and secure. We use JWT authentication
                and follow industry best practices for data protection.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <div className="text-center">
        <h3 className="mb-4">Ready to take control of your finances?</h3>
        <p className="text-muted mb-4">
          Join thousands of users who are already managing their expenses smarter.
        </p>
        <div className="d-flex justify-content-center gap-3">
          <a href="/register" className="btn btn-primary btn-lg">
            Get Started Free
          </a>
          <a href="/login" className="btn btn-outline-primary btn-lg">
            Sign In
          </a>
        </div>
      </div>
    </Container>
  );
};

export default Home;