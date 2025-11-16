import React, { useContext } from 'react';
import { Typography, Box, Grid } from '@mui/material';
import AuthContext from '../context/AuthContext';
import Weather from '../components/Weather';
import NewsFeed from '../components/NewsFeed';
import { useTranslation } from 'react-i18next';

const HomePage = () => {
    const { user } = useContext(AuthContext);
    const { t } = useTranslation();

    return (
        <Box sx={{ my: 4 }}>
            {user ? (
                // --- LOGGED-IN VIEW ---
                // Grid layout for the dashboard
                <Grid container spacing={4}>
                    <Grid item xs={12} md={4}>
                        <Weather />
                    </Grid>
                    <Grid item xs={12} md={8}>
                        <NewsFeed />
                    </Grid>
                </Grid>
            ) : (
                // --- LOGGED-OUT VIEW ---
                // Simple welcome text that will appear over the global watermark
                <Box sx={{ 
                    textAlign: 'center', 
                    padding: { xs: 2, md: 6 }, 
                    // Add a subtle background for readability over the watermark
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                    borderRadius: 2
                }}>
                    <Typography 
                        variant="h2" 
                        component="h1" 
                        gutterBottom 
                        sx={{ fontWeight: 'bold', color: 'primary.main' }}
                    >
                        {t('home.welcome')}
                    </Typography>
                    <Typography 
                        variant="h5" 
                        sx={{ color: 'text.secondary', fontStyle: 'italic' }}
                    >
                        {t('home.tagline')}
                    </Typography>
                    <Typography 
                        variant="h6" 
                        sx={{ mt: 3, color: 'text.primary' }}
                    >
                        {t('home.loginPrompt')}
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default HomePage;

