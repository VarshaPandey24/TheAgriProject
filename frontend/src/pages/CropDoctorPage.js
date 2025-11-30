import React, { useState } from 'react';
import { Typography, Box, Container, CircularProgress, Alert } from '@mui/material';
import ImageUpload from '../components/ImageUpload';
import AnalysisResults from '../components/AnalysisResults';
import { useTranslation } from 'react-i18next'; 

const CropDoctorPage = () => {
    const [analysisData, setAnalysisData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const { t } = useTranslation(); 

    const handleAnalysisComplete = (data) => {
        setIsLoading(false);
        if (data.error) {
            setError(data.error);
            setAnalysisData(null);
        } else {
            setAnalysisData(data);
            setError(null);
        }
    };

    const handleAnalysisStart = () => {
        setIsLoading(true);
        setError(null);
        setAnalysisData(null);
    };

    return (
        <Container maxWidth="md">
            <Box sx={{ my: 4, textAlign: 'center' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    {t('cropDoctor.title')}
                </Typography>
                <Typography variant="h6">
                    {t('cropDoctor.description')}
                </Typography>

                <ImageUpload
                    onAnalysisStart={handleAnalysisStart}
                    onAnalysisComplete={handleAnalysisComplete}
                />

                {isLoading && (
                    <Box sx={{ mt: 4 }}>
                        <CircularProgress />
                        <Typography>Analyzing your image... This may take a moment.</Typography>
                    </Box>
                )}

                {error && (
                    <Alert severity="error" sx={{ mt: 4 }}>
                        {error}
                    </Alert>
                )}

                {analysisData && (
                    <AnalysisResults data={analysisData} />
                )}
            </Box>
        </Container>
    );
};

export default CropDoctorPage;