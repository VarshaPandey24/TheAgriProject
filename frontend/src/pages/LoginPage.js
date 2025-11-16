import React, { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
} from '@mui/material';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { loginUser } = useContext(AuthContext);
  const handleSubmit = (event) => {
    event.preventDefault();
    loginUser(username, password);
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Card sx={{ minWidth: 275, boxShadow: 3 }}>
          <CardContent sx={{ padding: '2rem' }}>
            <Typography component="h1" variant="h5" align="center">
              Login
            </Typography>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default LoginPage;