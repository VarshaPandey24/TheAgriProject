import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'; 
import HomePage from './pages/HomePage'; 
import LoginPage from './pages/LoginPage'; 
import RegisterPage from './pages/RegisterPage'; 
import { Container, CssBaseline } from '@mui/material';
import { AuthProvider } from './context/AuthContext';
import CropDoctorPage from './pages/CropDoctorPage';
import SchemePage from './pages/SchemePage';
import ChatbotWidget from './components/ChatbotWidget';

function App() {
  return (
    <Router>
      <AuthProvider> 
      <CssBaseline />
      <Navbar />
      <Container sx={{ marginTop: '2rem' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/crop-doctor" element={<CropDoctorPage />} />
          <Route path="/schemes" element={<SchemePage />}/>
        </Routes>
      </Container>
      <ChatbotWidget />
       </AuthProvider> 
    </Router>
  );
}

export default App;