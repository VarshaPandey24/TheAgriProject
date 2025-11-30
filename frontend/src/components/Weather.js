import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import WbCloudyIcon from '@mui/icons-material/WbCloudy';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import WaterDropIcon from '@mui/icons-material/WaterDrop';

const Weather = () => {
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWeatherData = (params) => {
            const query = new URLSearchParams(params).toString();
            setLoading(true); 
            fetch(`/api/weather/?${query}`)
                .then(response => {
                    if (!response.ok) throw new Error('Weather data not found');
                    return response.json();
                })
                .then(data => {
                    setWeatherData(data);
                    setLoading(false);
                })
                .catch(error => {
                    console.error("Error fetching weather:", error);
                    setLoading(false);
                    if (params.city !== 'Delhi') {
                        fetchWeatherData({ city: 'Delhi' });
                    }
                });
        };

        const getLocation = () => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => { 
                        fetchWeatherData({ lat: position.coords.latitude, lon: position.coords.longitude });
                    },
                    (error) => { 
                        console.log("Geolocation error, defaulting to Delhi.", error);
                        fetchWeatherData({ city: 'Delhi' }); 
                    }
                );
            } else {
                console.log("Geolocation not supported, defaulting to Delhi.");
                fetchWeatherData({ city: 'Delhi' });
            }
        };
        
        getLocation();
    }, []); 

    const getWeatherIcon = (condition) => {
        if (!condition) return <WbCloudyIcon sx={{ fontSize: 60, color: 'text.secondary' }} />;
        const lowerCaseCondition = condition.toLowerCase();

        if (lowerCaseCondition.includes('clear')) return <WbSunnyIcon sx={{ fontSize: 60, color: '#fbc02d' }} />;
        if (lowerCaseCondition.includes('clouds')) return <WbCloudyIcon sx={{ fontSize: 60, color: 'text.secondary' }} />;
        if (lowerCaseCondition.includes('rain') || lowerCaseCondition.includes('drizzle')) return <WaterDropIcon sx={{ fontSize: 60, color: '#1976d2' }} />;
        if (lowerCaseCondition.includes('thunderstorm')) return <ThunderstormIcon sx={{ fontSize: 60, color: '#37474f' }} />;
        
        return <WbCloudyIcon sx={{ fontSize: 60, color: 'text.secondary' }} />;
    };

    if (loading) {
        return <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}><CircularProgress color="primary" /></Box>;
    }
    
    if (!weatherData || weatherData.error) {
        return <Typography>Could not load weather data.</Typography>;
    }

    return (
        <Card sx={{ height: '100%' }}> 
            <CardContent>
                <Typography variant="h5" component="div">{weatherData.city}</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
                    {getWeatherIcon(weatherData.main_condition)}
                    <Typography variant="h3" sx={{ ml: 2, color: 'text.primary', fontWeight: 600 }}>
                        {Math.round(weatherData.temperature)}°C
                    </Typography>
                </Box>
                <Typography variant="body1" sx={{ textTransform: 'capitalize' }}>{weatherData.description}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>Chance of Rain: {Math.round(weatherData.chance_of_rain)}%</Typography>
                <Typography variant="body2" color="text.secondary">Humidity: {weatherData.humidity}%</Typography>
                <Typography variant="body2" color="text.secondary">Wind: {weatherData.wind_speed} m/s</Typography>
            </CardContent>
        </Card>
    );
};

export default Weather;

