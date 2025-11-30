// frontend/src/context/AuthContext.js
import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => 
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
  );
  
  const [user, setUser] = useState(() => 
    localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')).access : null
  );

  const navigate = useNavigate();

  const loginUser = async (username, password) => {
    const response = await fetch('/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    console.log('Login Response Status:', response.status);
    console.log('Response Data:', data);

    if (response.ok) { 
      setAuthTokens(data);
      const decodedUser = jwtDecode(data.access);
      setUser(decodedUser);
      localStorage.setItem('authTokens', JSON.stringify(data));
      navigate('/');
    } else if (response.status === 401) {
      alert('Login failed: Invalid username or password. Please try again.');
    } else {
      alert('An unknown error occurred. Please try again later.');
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  const contextData = {
    user: user,
    authTokens: authTokens,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};