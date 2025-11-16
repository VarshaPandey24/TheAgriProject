// frontend/src/pages/SchemePage.js
import React, { useState, useEffect } from 'react';
import { 
    Box, 
    Typography, 
    CircularProgress, 
    Accordion, 
    AccordionSummary, 
    AccordionDetails,
    Paper,
    Button, // Import Button
    List, // Import List
    ListItem, // Import ListItem
    ListItemIcon,
    ListItemText
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle'; // Icon for bullets

const SchemePage = () => {
    const [schemes, setSchemes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/api/schemes/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setSchemes(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching schemes:", error);
                setError("Failed to load schemes.");
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return <Typography color="error" sx={{ mt: 3 }}>{error}</Typography>;
    }

    return (
        <Box sx={{ my: 4 }}>
            <Typography variant="h4" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                Government Schemes for Farmers
            </Typography>
            
            {schemes.length === 0 ? (
                <Typography sx={{ mt: 3 }}>
                    No government schemes are available at this time.
                </Typography>
            ) : (
                <Box sx={{ mt: 3 }}>
                    {schemes.map((scheme) => (
                        <Accordion 
                            key={scheme.id} 
                            component={Paper} 
                            elevation={1} 
                            sx={{ mb: 1.5, '&:before': { display: 'none' } }}
                        >
                            <AccordionSummary
                                expandIcon={<ExpandMoreIcon color="primary" />}
                                aria-controls={`panel${scheme.id}-content`}
                                id={`panel${scheme.id}-header`}
                            >
                                <Box>
                                    {/* 1. Title: Bold and Bigger */}
                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                        {scheme.title}
                                    </Typography>
                                    {/* 2. Summary: Bold and simple */}
                                    <Typography variant="body1" color="text.secondary" sx={{ fontWeight: '500', mt: 1 }}>
                                        {scheme.summary}
                                    </Typography>
                                </Box>
                            </AccordionSummary>
                            <AccordionDetails sx={{ borderTop: '1px solid #eee', px: 3 }}>
                                
                                {/* 3. Details (as bullets) */}
                                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                                    Details
                                </Typography>
                                <List dense>
                                    {scheme.details && scheme.details.map((item, index) => (
                                        <ListItem key={index} sx={{ py: 0 }}>
                                            <ListItemIcon sx={{ minWidth: '32px' }}><CheckCircleIcon color="primary" fontSize="small" /></ListItemIcon>
                                            <ListItemText primary={item} />
                                        </ListItem>
                                    ))}
                                </List>

                                {/* 4. Eligibility (as bullets) */}
                                <Typography variant="h6" sx={{ fontWeight: 'bold', mt: 2, mb: 1 }}>
                                    Eligibility
                                </Typography>
                                <List dense>
                                    {scheme.eligibility && scheme.eligibility.map((item, index) => (
                                        <ListItem key={index} sx={{ py: 0 }}>
                                            <ListItemIcon sx={{ minWidth: '32px' }}><CheckCircleIcon color="primary" fontSize="small" /></ListItemIcon>
                                            <ListItemText primary={item} />
                                        </ListItem>
                                    ))}
                                </List>

                                {/* 5. Apply Link (as a button) */}
                                {scheme.apply_link && (
                                    <Button 
                                        variant="contained" 
                                        color="primary" 
                                        href={scheme.apply_link}
                                        target="_blank" // Opens in a new tab
                                        rel="noopener noreferrer"
                                        sx={{ mt: 3 }}
                                    >
                                        Apply Now
                                    </Button>
                                )}
                            </AccordionDetails>
                        </Accordion>
                    ))}
                </Box>
            )}
        </Box>
    );
};

export default SchemePage;