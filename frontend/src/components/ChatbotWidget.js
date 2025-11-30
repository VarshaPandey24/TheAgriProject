import React, { useState, useRef, useEffect, useContext } from 'react';
import { Box, Fab, Paper, Typography, TextField, IconButton } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';
import SendIcon from '@mui/icons-material/Send';
import AuthContext from '../context/AuthContext';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import CircularProgress from '@mui/material/CircularProgress';

const ChatbotWidget = () => {
    const [open, setOpen] = useState(false);
    const [messages, setMessages] = useState([
        { sender: 'ai', text: 'नमस्ते! मैं किसान मित्र हूँ। आप सरकारी योजनाओं के बारे में क्या पूछना चाहते हैं?' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);
    const { authTokens, user } = useContext(AuthContext);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (inputValue.trim() === '') return;

        const userMessage = { sender: 'user', text: inputValue };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setLoading(true);

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authTokens.access}`
                },
                body: JSON.stringify({ query: inputValue })
            });

            if (!response.ok) {
                throw new Error('Failed to get a response from the server.');
            }

            const data = await response.json();
            const aiMessage = { sender: 'ai', text: data.answer };
            setMessages(prev => [...prev, aiMessage]);

        } catch (error) {
            console.error("Chat error:", error);
            const errorMessage = { sender: 'ai', text: 'माफ़ कीजिये, कुछ गड़बड़ हो गई है। कृपया बाद में प्रयास करें।' };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const toggleChat = () => {
        setOpen(!open);
    };
    if (!user) {
        return null;
    }

    return (
        <>
            <Fab
                color="primary"
                sx={{ 
                    position: 'fixed', 
                    bottom: 24, 
                    right: 24, 
                    zIndex: 1000 
                }}
                onClick={toggleChat}
            >
                {open ? <CloseIcon /> : <ChatIcon />}
            </Fab>

            {open && (
                <Paper
                    elevation={10}
                    sx={{
                        position: 'fixed',
                        bottom: 96,
                        right: 24, 
                        width: { xs: 'calc(100% - 48px)', sm: 350 },
                        height: { xs: '60%', sm: 450 },
                        zIndex: 1000,
                        display: 'flex',
                        flexDirection: 'column',
                        borderRadius: '12px',
                        overflow: 'hidden'
                    }}
                >
                    <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white', display: 'flex', alignItems: 'center' }}>
                        <SmartToyIcon sx={{ mr: 1 }} />
                        <Typography variant="h6">Kisan Mitra Chat</Typography>
                    </Box>

                    <Box sx={{ flexGrow: 1, p: 2, overflowY: 'auto', backgroundColor: 'background.default' }}>
                        {messages.map((msg, index) => (
                            <Box
                                key={index}
                                sx={{
                                    display: 'flex',
                                    justifyContent: msg.sender === 'ai' ? 'flex-start' : 'flex-end',
                                    mb: 1.5,
                                }}
                            >
                                {msg.sender === 'ai' && <SmartToyIcon color="primary" sx={{ mr: 1 }} />}
                                <Paper
                                    elevation={1}
                                    sx={{
                                        p: 1.5,
                                        borderRadius: '10px',
                                        bgcolor: msg.sender === 'ai' ? 'white' : 'primary.light',
                                        color: msg.sender === 'ai' ? 'black' : 'white',
                                        maxWidth: '80%'
                                    }}
                                >
                                    <Typography variant="body1">{msg.text}</Typography>
                                </Paper>
                                {msg.sender === 'user' && <PersonIcon color="action" sx={{ ml: 1 }} />}
                            </Box>
                        ))}
                        {loading && (
                            <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1.5 }}>
                                <SmartToyIcon color="primary" sx={{ mr: 1 }} />
                                <Paper elevation={1} sx={{ p: 1.5, borderRadius: '10px', bgcolor: 'white' }}>
                                    <CircularProgress size={20} />
                                </Paper>
                            </Box>
                        )}
                        <div ref={messagesEndRef} />
                    </Box>
                    <Box sx={{ p: 1.5, borderTop: '1px solid #ddd', display: 'flex' }}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            size="small"
                            placeholder="हिंदी में एक सवाल पूछें..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        />
                        <IconButton color="primary" onClick={handleSend} disabled={loading}>
                            <SendIcon />
                        </IconButton>
                    </Box>
                </Paper>
            )}
        </>
    );
};

export default ChatbotWidget;