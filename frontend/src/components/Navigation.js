import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useAuth } from '../context/AuthContext';
import { FaWallet, FaChartLine, FaUser, FaSignOutAlt } from 'react-icons/fa';

const Navigation = () => {
  const { isAuthenticated, logout, user } = useAuth();

  if (!isAuthenticated) {
    return null;
  }

  return (
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <LinkContainer to="/dashboard">
          <Navbar.Brand>
            <FaWallet className="me-2" />
            Smart Expense Tracker
          </Navbar.Brand>
        </LinkContainer>

        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <LinkContainer to="/dashboard">
              <Nav.Link>Dashboard</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/expenses">
              <Nav.Link>Expenses</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/analytics">
              <Nav.Link>
                <FaChartLine className="me-1" />
                Analytics
              </Nav.Link>
            </LinkContainer>
          </Nav>

          <Nav>
            <LinkContainer to="/profile">
              <Nav.Link>
                <FaUser className="me-1" />
                {user?.first_name || user?.username}
              </Nav.Link>
            </LinkContainer>
            <Button
              variant="outline-danger"
              size="sm"
              onClick={logout}
              className="ms-2"
            >
              <FaSignOutAlt className="me-1" />
              Logout
            </Button>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;