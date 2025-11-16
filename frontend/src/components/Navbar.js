import React, { useContext } from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import logo from '../logoImage.png'; 

const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const { t, i18n } = useTranslation();

  const handleLanguageChange = () => {
    const newLang = i18n.language === 'en' ? 'hi' : 'en';
    i18n.changeLanguage(newLang);
  };

  // --- 1. Define a style for our larger buttons ---
  const navButtonSx = {
    my: 1,
    mx: 0.5,
    padding: '8px 16px', // Increase padding
    fontSize: '1rem',    // Increase font size
    fontWeight: 500,     // Make text a bit bolder
  };

  return (
    <AppBar 
      position="static" 
      color="default" 
      elevation={0} 
      sx={{ borderBottom: '1px solid #e0e0e0' }}
    >
      <Toolbar disableGutters sx={{ paddingRight: '16px' }}> {/* Add padding back to the right side */}
        
        {/* Logo and Title */}
        <Typography 
          variant="h6" 
          component={RouterLink} 
          to="/" 
          sx={{ 
            flexGrow: 1, 
            color: 'primary.main', 
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            fontWeight: 'bold',
            paddingLeft: '16px' 
          }}
        >
          <img 
            src={logo} 
            alt="Kisan Mitra logo" 
            style={{ 
              height: '100px', 
              marginRight: '12px' 
            }} 
          />
          
        </Typography>

        {/* --- 2. Apply the 'navButtonSx' style to the language button --- */}
        <Button 
          variant="outlined" 
          color="primary"
          onClick={handleLanguageChange}
          sx={{ ...navButtonSx, mx: 1.5 }} // Use the style, keep margin
        >
          {i18n.language === 'en' ? 'हिन्दी' : 'English'}
        </Button>

        {/* Auth Links */}
        {user ? (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {/* --- 3. Apply the 'navButtonSx' style to the other buttons --- */}
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/crop-doctor"
              sx={navButtonSx} // Apply here
            >
              {t('nav.cropDoctor')}
            </Button>
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/schemes"
              sx={navButtonSx}
            >
              Govt. Schemes
            </Button>
            
            <Typography 
              component="span" 
              sx={{ 
                mr: 1, 
                ml: 1, 
                color: 'text.secondary', 
                display: { xs: 'none', sm: 'inline' },
                fontSize: '1rem', // Also increase "Hello" text size
              }}
            >
              {t('nav.hello')}, {user.username}
            </Typography>

            <Button 
              color="primary" 
              onClick={logoutUser}
              sx={navButtonSx} // Apply here
            >
              {t('nav.logout')}
            </Button>
          </Box>
        ) : (
          <Box>
            {/* --- 4. Apply the 'navButtonSx' style to the login/register buttons --- */}
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/login"
              sx={navButtonSx} // Apply here
            >
              {t('nav.login')}
            </Button>
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/register"
              sx={navButtonSx} // Apply here
            >
              {t('nav.register')}
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;

