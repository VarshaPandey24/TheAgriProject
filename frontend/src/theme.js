import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2e7d32', // Strong green
    },
    secondary: {
      main: '#81c784', // Lighter green
    },
    background: {
      default: '#f8f9fa', // Off-white background
      paper: '#ffffff', // Solid white for paper/cards
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
    // --- THIS IS THE GLOBAL WATERMARK ---
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
    // --- THIS IS THE FIX ---
    // We are making the AppBar solid white
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', // Solid white
          color: '#2e7d32', // Green text
          boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.06)', // Subtle shadow
        },
      },
    },
    // We are making Cards solid white
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', // Solid white
          boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
          borderRadius: '12px',
        },
      },
    },
    // We are also making Paper (used for results) solid white
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff', // Solid white
          boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
          borderRadius: '12px',
        },
      },
    },
  },
});

export default theme;

