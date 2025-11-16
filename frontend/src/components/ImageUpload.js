import React, { useState, useContext } from 'react';
import { Box, Button, Typography, Select, MenuItem, FormControl, InputLabel, TextField } from '@mui/material';
import AuthContext from '../context/AuthContext';
import { useTranslation } from 'react-i18next'; // 1. Import the hook

const ImageUpload = ({ onAnalysisStart, onAnalysisComplete }) => {
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [cropName, setCropName] = useState('');
    const [district, setDistrict] = useState('');
    const [state, setState] = useState('');
    
    const { authTokens } = useContext(AuthContext);
    const { i18n } = useTranslation(); // 2. Get the i18n instance

    const handleImageChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            let file = e.target.files[0];
            setImage(file);
            setImagePreview(URL.createObjectURL(file));
        }
    };

    const handleCropChange = (e) => setCropName(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!image || !cropName || !district || !state) {
            alert("Please fill in all fields: image, crop, district, and state.");
            return;
        }
        
        onAnalysisStart();
        
        const currentLang = i18n.language; // 3. Get the current language (e.g., 'en' or 'hi')

        const formData = new FormData();
        formData.append('image', image);
        formData.append('crop_name', cropName);
        formData.append('district', district);
        formData.append('state', state);
        formData.append('lang', currentLang); // 4. Add the language to the form data

        try {
            const response = await fetch('/api/crop-health/', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authTokens.access}` },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An unknown error occurred.');
            }
            onAnalysisComplete(data);
            
        } catch (error) {
            console.error("Upload failed:", error);
            onAnalysisComplete({ error: error.message });
        }
    };

    
    const cropOptions = [
        'Rice', 'Wheat', 'Potato', 'Cotton', 'Sugarcane', 'Other'
    ];

    return (
        <Box component="form" onSubmit={handleSubmit}sx={{ 
  mt: 3, 
  p: 2, 
  border: '1px dashed grey', 
  borderRadius: 2, 
  backgroundColor: 'white' 
}}>
            {/* ... (all your JSX for the form) ... */}
             <Button variant="contained" component="label">
                Upload Image
                <input type="file" hidden accept="image/*" onChange={handleImageChange} />
            </Button>

            {imagePreview && (
                <Box sx={{ my: 2, textAlign: 'center' }}>
                    <Typography>Image Preview:</Typography>
                    <img src={imagePreview} alt="Crop preview" style={{ maxWidth: '100%', maxHeight: '300px', objectFit: 'contain' }} />
                </Box>
            )}

            <FormControl fullWidth sx={{ my: 2 }}>
                <InputLabel id="crop-select-label">Select Crop</InputLabel>
                <Select labelId="crop-select-label" value={cropName} label="Select Crop" onChange={handleCropChange}>
                    {cropOptions.map((crop) => (
                        <MenuItem key={crop} value={crop}>{crop}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <TextField label="District" value={district} onChange={(e) => setDistrict(e.target.value)} fullWidth sx={{ my: 1 }} />
            <TextField label="State" value={state} onChange={(e) => setState(e.target.value)} fullWidth sx={{ my: 1 }} />

            <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={!image || !cropName || !district || !state}
                sx={{ mt: 2 }}
            >
                Get Diagnosis
            </Button>
        </Box>
    );
};

export default ImageUpload;