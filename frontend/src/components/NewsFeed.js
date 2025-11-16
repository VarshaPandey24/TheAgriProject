import React, { useState, useEffect } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import {
    Box,
    Typography,
    Card,
    CardContent,
    CircularProgress,
    Modal,
    Fade,
    IconButton,
    Link,
    Backdrop,
    ToggleButtonGroup,
    ToggleButton,
    CardMedia, // Import CardMedia for images
    Paper,      // Import Paper for the header background
    CardActionArea // Import CardActionArea for a better click effect
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward'; // For the arrow icon

// Updated language list based on your previous request
const languages = [
    { code: 'en', name: 'English' }, { code: 'hi', name: 'हिन्दी' }
];

const NewsFeed = () => {
    const [articles, setArticles] = useState([]);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);
    const [selectedArticle, setSelectedArticle] = useState(null);
    const [language, setLanguage] = useState('en');

    const fetchArticles = (lang = language, pageNum = 1, isNewLang = false) => {
        // Reset hasMore to true when fetching new language
        if (isNewLang) {
            setHasMore(true);
        }

        fetch(`/api/news/?page=${pageNum}&lang=${lang}`)
            .then(res => res.json())
            .then(data => {
                if (data.articles && data.articles.length > 0) {
                    setArticles(isNewLang ? data.articles : prev => [...prev, ...data.articles]);
                    // Check if we have all the results
                    const totalLoaded = isNewLang ? data.articles.length : articles.length + data.articles.length;
                    setHasMore(totalLoaded < data.totalResults);
                } else {
                    setHasMore(false); // No more articles to load
                }
            })
            .catch(err => {
                console.error("Error fetching news:", err);
                setHasMore(false);
            });
    };

    // Effect for the *initial* load
    useEffect(() => {
        fetchArticles('en', 1, true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // Runs only once on mount

    // Handler for language change - This logic is corrected
    const handleLanguageChange = (event, newLanguage) => {
        if (newLanguage !== null && newLanguage !== language) {
            setLanguage(newLanguage);
            setArticles([]); // Clear existing articles
            setPage(1); // Reset page number
            // Call fetchArticles immediately with the new language and reset flags
            fetchArticles(newLanguage, 1, true);
        }
    };
    
    // This is called by InfiniteScroll to load more
    const loadMoreArticles = () => {
        const nextPage = page + 1;
        setPage(nextPage);
        fetchArticles(language, nextPage, false); // 'false' means we append, not replace
    };

    // Modal logic
    const handleOpenModal = (article) => setSelectedArticle(article);
    const handleCloseModal = () => setSelectedArticle(null);
    // Use theme's paper background for modal
    const modalStyle = { 
        position: 'absolute', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: { xs: '90%', md: 600 }, 
        bgcolor: 'background.paper', 
        borderRadius: '12px', 
        boxShadow: 24, 
        p: 4, 
        border: 'none' 
    };

    return (
        <Box sx={{ mt: 4 }}>
            {/* --- WRAP HEADER IN OPAQUE PAPER --- */}
            <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h4" gutterBottom>Agricultural News</Typography>

                <ToggleButtonGroup 
                    value={language} 
                    exclusive 
                    onChange={handleLanguageChange} 
                    aria-label="language selection" 
                    sx={{ mb: 2, flexWrap: 'wrap' }}
                >
                    {languages.map((lang) => (
                        <ToggleButton key={lang.code} value={lang.code} aria-label={lang.name}>
                            {lang.name}
                        </ToggleButton>
                    ))}
                </ToggleButtonGroup>
            </Paper>

            <InfiniteScroll
                dataLength={articles.length}
                next={loadMoreArticles}
                hasMore={hasMore}
                loader={<Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}><CircularProgress /></Box>}
                endMessage={<Typography sx={{ textAlign: 'center', my: 2 }}><b>You have seen all the news!</b></Typography>}
                key={language} // Add key to force re-render on language change
            >
                {articles.map((article, index) => (
                    <Card key={index} sx={{ mb: 2, display: 'flex', flexDirection: 'column' }}>
                        <CardActionArea onClick={() => handleOpenModal(article)}>
                            {/* --- ADD CARDMEDIA FOR IMAGE --- */}
                            {article.urlToImage && (
                                <CardMedia
                                    component="img"
                                    height="200"
                                    image={article.urlToImage}
                                    alt={article.title}
                                    // Handle image errors
                                    onError={(e) => { e.target.style.display = 'none'; }} 
                                />
                            )}
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    {article.title}
                                </Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                                    {article.source.name} - {new Date(article.publishedAt).toLocaleDateString()}
                                </Typography>
                                <Box sx={{ display: 'flex', alignItems: 'center', color: 'primary.main' }}>
                                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                                        Read More
                                    </Typography>
                                    <ArrowForwardIcon sx={{ ml: 0.5, fontSize: '1rem' }} />
                                </Box>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                ))}
            </InfiniteScroll>

            {/* --- Modal Component --- */}
            <Modal 
                open={selectedArticle !== null} 
                onClose={handleCloseModal} 
                closeAfterTransition 
                slots={{ backdrop: Backdrop }} 
                slotProps={{ backdrop: { timeout: 500 } }}
            >
                <Fade in={selectedArticle !== null}>
                    <Box sx={modalStyle}>
                        <IconButton 
                            aria-label="close" 
                            onClick={handleCloseModal} 
                            sx={{ position: 'absolute', right: 8, top: 8 }}
                        >
                            <CloseIcon />
                        </IconButton>
                        <Typography variant="h5" component="h2">
                            {selectedArticle?.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                            By {selectedArticle?.author || selectedArticle?.source.name}
                        </Typography>
                        {/* --- ADD IMAGE TO MODAL --- */}
                        {selectedArticle?.urlToImage && (
                            <Box
                                component="img"
                                src={selectedArticle.urlToImage}
                                alt={selectedArticle.title}
                                sx={{
                                    width: '100%',
                                    maxHeight: '300px',
                                    objectFit: 'cover',
                                    borderRadius: '8px',
                                    mt: 2
                                }}
                            />
                        )}
                        <Typography sx={{ mt: 2 }}>
                            {selectedArticle?.description}
                        </Typography>
                        <Link 
                            href={selectedArticle?.url} 
                            target="_blank" 
                            rel="noopener" 
                            sx={{ mt: 2, display: 'block', fontWeight: 'bold' }}
                        >
                            Read Full Article
                        </Link>
                    </Box>
                </Fade>
            </Modal>
        </Box>
    );
};

export default NewsFeed;

