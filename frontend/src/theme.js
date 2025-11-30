import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2e7d32', 
    },
    secondary: {
      main: '#81c784', 
    },
    background: {
      default: '#f8f9fa', 
      paper: '#ffffff', 
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h1: { color: '#2e7d32' },
    h2: { color: '#2e7d32' },
    h3: { color: '#2e7d32' },
    h4: { color: '#2e7d32' },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          '&::before': { 
            content: '""',
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: 'url(/c.jpg)', 
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            opacity: 0.8, 
            zIndex: -1, 
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', 
          color: '#2e7d32', 
          boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.06)', 
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', 
          boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
          borderRadius: '12px',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', 
          boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
          borderRadius: '12px',
        },
      },
    },
  },
});

export default theme;

