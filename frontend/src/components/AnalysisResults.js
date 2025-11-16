import React from 'react';
import {
    Box, Typography, Paper, Grid, Link, Card, CardMedia, CardContent
} from '@mui/material';

const AnalysisResults = ({ data }) => {
    // Helper function to render list items safely
    const renderList = (items) => {
        if (!items || !Array.isArray(items)) {
            return <Typography>No information available.</Typography>;
        }
        return (
            <ul style={{ paddingLeft: '20px' }}>
                {items.map((item, index) => (
                    <li key={index}><Typography>{item}</Typography></li>
                ))}
            </ul>
        );
    };

    return (
        <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
            <Typography variant="h4" color="primary" gutterBottom>
                Diagnosis Results
            </Typography>

            {/* --- Disease Name --- */}
            <Box sx={{ mb: 3 }}>
                <Typography variant="h6">Identified Disease:</Typography>
                <Typography variant="h5" color="error">
                    {data.disease_name || 'Unknown'}
                </Typography>
            </Box>

            {/* --- Gemini Analysis --- */}
            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Symptoms</Typography>
                    {renderList(data.analysis?.symptoms)}
                </Grid>
                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Potential Causes</Typography>
                    {renderList(data.analysis?.causes)}
                </Grid>
                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Remedies</Typography>
                    {renderList(data.analysis?.remedies)}
                </Grid>
            </Grid>

            {/* --- YouTube Videos --- */}
            <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                    Related Videos 
                </Typography>
                <Box sx={{
                    display: 'flex',
                    overflowX: 'auto',
                    gap: 2,
                    pb: 1
                }}>
                    {data.videos && data.videos.length > 0 ? (
                        data.videos.map((video) => (
                            <Link
                                key={video.videoId}
                                href={`https://www.youtube.com/watch?v=${video.videoId}`}
                                target="_blank"
                                rel="noopener"
                                underline="none"
                            >
                                <Card sx={{ minWidth: 200 }}>
                                    <CardMedia
                                        component="img"
                                        height="120"
                                        image={video.thumbnailUrl}
                                        alt={video.title}
                                    />
                                    <CardContent>
                                        <Typography variant="body2" sx={{
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            display: '-webkit-box',
                                            WebkitLineClamp: 2,
                                            WebkitBoxOrient: 'vertical'
                                        }}>
                                            {video.title}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Link>
                        ))
                    ) : (
                        <Typography>No videos found.</Typography>
                    )}
                </Box>
            </Box>
        </Paper>
    );
};

export default AnalysisResults;