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

  const navButtonSx = {
    my: 1,
    mx: 0.5,
    padding: '8px 16px', 
    fontSize: '1rem',   
    fontWeight: 500,    
  };

  return (
    <AppBar 
      position="static" 
      color="default" 
      elevation={0} 
      sx={{ borderBottom: '1px solid #e0e0e0' }}
    >
      <Toolbar disableGutters sx={{ paddingRight: '16px' }}> 
        
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
        <Button 
          variant="outlined" 
          color="primary"
          onClick={handleLanguageChange}
          sx={{ ...navButtonSx, mx: 1.5 }} 
        >
          {i18n.language === 'en' ? 'हिन्दी' : 'English'}
        </Button>

        {user ? (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/crop-doctor"
              sx={navButtonSx} 
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
                fontSize: '1rem', 
              }}
            >
              {t('nav.hello')}, {user.username}
            </Typography>

            <Button 
              color="primary" 
              onClick={logoutUser}
              sx={navButtonSx} 
            >
              {t('nav.logout')}
            </Button>
          </Box>
        ) : (
          <Box>
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/login"
              sx={navButtonSx} 
            >
              {t('nav.login')}
            </Button>
            <Button 
              color="primary" 
              component={RouterLink} 
              to="/register"
              sx={navButtonSx} 
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

