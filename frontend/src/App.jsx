import React, { useState, useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { 
  Box, 
  Container, 
  Typography, 
  Card, 
  Grid, 
  Button, 
  Stack, 
  Divider, 
  Alert, 
  CircularProgress,
  Chip,
  TextField
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { jobDiscoveryApi } from './services/api';

// Import layout components
import Header from './components/common/Header';
import Footer from './components/common/Footer';

// Import animations
import { fadeIn, slideUp, staggerContainer, scaleUp } from './utils/transitions';

// Import forms
import JobSearchForm from './components/forms/JobSearchForm';

// Import global styles
import './styles/global.css';
// Motion components
const MotionBox = motion(Box);
const MotionTypography = motion(Typography);
const MotionCard = motion(Card);
const MotionButton = motion(Button);

// Styled components for Apple-like design
const HeroSection = styled(Box)(({ theme }) => ({
  textAlign: 'center',
  padding: theme.spacing(16, 2, 12),
  [theme.breakpoints.down('md')]: {
    padding: theme.spacing(10, 2, 8),
  },
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-start',
  transition: 'transform 0.3s ease-in-out',
  border: 'none',
  backgroundColor: 'transparent',
  '&:hover': {
    transform: 'translateY(-4px)',
  },
}));

const AppleButton = styled(Button)(({ theme }) => ({
  borderRadius: 8,
  padding: '12px 24px',
  fontWeight: 500,
  textTransform: 'none',
  fontSize: '1rem',
  transition: 'all 0.2s ease',
}));

// Clean UI components

// Placeholder pages with Apple-inspired design
const Dashboard = () => {
  // Animation hooks for scroll-triggered animations
  const [heroRef, heroInView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  
  const [featuresRef, featuresInView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  
  const [whyChooseRef, whyChooseInView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <MotionBox
      variants={fadeIn}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <Box ref={heroRef} sx={{ py: { xs: 8, md: 12 } }}>
        <Container maxWidth="lg">
          <Box sx={{ 
            textAlign: 'center', 
            maxWidth: 800, 
            mx: 'auto',
            px: 2
          }}>
            <MotionTypography 
              variant="h1" 
              sx={{ 
                fontWeight: 600, 
                fontSize: { xs: '2.5rem', md: '3.5rem' },
                letterSpacing: '-0.025em',
                mb: 3,
              }}
              variants={slideUp}
              initial="initial"
              animate={heroInView ? "animate" : "initial"}
              transition={{ delay: 0.2 }}
            >
              Agentic AI Job System
            </MotionTypography>
            
            <MotionTypography 
              variant="h5" 
              color="text.secondary" 
              sx={{ 
                maxWidth: 600, 
                mx: 'auto', 
                mb: 6,
                fontWeight: 400,
              }}
              variants={slideUp}
              initial="initial"
              animate={heroInView ? "animate" : "initial"}
              transition={{ delay: 0.3 }}
            >
              Intelligent automation for your entire job search process.
            </MotionTypography>
            
            <MotionBox
              component={Stack}
              direction={{ xs: 'column', sm: 'row' }} 
              spacing={2} 
              justifyContent="center"
              sx={{ mb: 4 }}
              variants={staggerContainer}
              initial="initial"
              animate={heroInView ? "animate" : "initial"}
            >
              <MotionButton 
                component={AppleButton}
                variant="contained" 
                size="large"
                variants={scaleUp}
                whileHover="hover"
                whileTap="tap"
              >
                Get Started
              </MotionButton>
              
              <MotionButton 
                component={AppleButton}
                variant="outlined" 
                size="large"
                variants={scaleUp}
                whileHover="hover"
                whileTap="tap"
              >
                Learn More
              </MotionButton>
            </MotionBox>
          </Box>
        </Container>
      </Box>

      <Divider sx={{ borderColor: '#d2d2d7' }} />

      <Box sx={{ py: 12, backgroundColor: '#ffffff' }} ref={featuresRef}>
        <Container maxWidth="lg">
          <MotionTypography 
            variant="h2" 
            align="center" 
            sx={{ 
              mb: 8,
              fontWeight: 600,
              fontSize: { xs: '2rem', md: '2.5rem' },
              letterSpacing: '-0.025em',
            }}
            variants={slideUp}
            initial="initial"
            animate={featuresInView ? "animate" : "initial"}
          >
            How It Works
          </MotionTypography>
          
          <MotionBox
            component={Grid}
            container
            spacing={6}
            variants={staggerContainer}
            initial="initial"
            animate={featuresInView ? "animate" : "initial"}
          >
            {[
              {
                title: 'Job Discovery',
                description: 'Our AI agents find the perfect job matches based on your skills and preferences.',
              },
              {
                title: 'Resume Analysis',
                description: 'Get insights on how to improve your resume and tailor it for specific positions.',
              },
              {
                title: 'Application Generator',
                description: 'Create personalized cover letters and application materials with a single click.',
              },
              {
                title: 'Submission Assistant',
                description: 'Automate the application submission process across multiple job platforms.',
              },
            ].map((feature, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <MotionCard
                  component={FeatureCard}
                  variants={scaleUp}
                  whileHover={{ y: -8, transition: { duration: 0.3 } }}
                >
                  <Typography 
                    variant="h2" 
                    sx={{ 
                      mb: 1,
                      fontWeight: 600,
                      fontSize: '2.5rem',
                      color: '#000000',
                    }}
                  >
                    {`0${index + 1}`}
                  </Typography>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      mb: 2,
                      fontWeight: 600,
                      color: '#000000',
                    }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </MotionCard>
              </Grid>
            ))}
          </MotionBox>
        </Container>
      </Box>

      <Divider sx={{ borderColor: '#d2d2d7' }} />

      <Box sx={{ py: 8, backgroundColor: 'background.subtle' }} ref={whyChooseRef}>
        <Container maxWidth="lg">
          <MotionTypography 
            variant="h2" 
            align="center" 
            sx={{ 
              mb: 8,
              fontWeight: 600,
              fontSize: { xs: '2rem', md: '2.5rem' },
              letterSpacing: '-0.025em',
            }}
            variants={slideUp}
            initial="initial"
            animate={whyChooseInView ? "animate" : "initial"}
          >
            Why Choose Agentic AI
          </MotionTypography>
          
          <Grid container spacing={4}>
            {[
              {
                title: "Intelligent Job Matching",
                description: "Our AI analyzes thousands of job postings to find the perfect match for your skills and career goals."
              },
              {
                title: "Resume Optimization",
                description: "Get personalized feedback that helps your resume stand out from the crowd."
              },
              {
                title: "Application Automation",
                description: "Streamline your application process with AI-powered tools that save you time and effort."
              }
            ].map((item, index) => (
              <Grid item xs={12} md={4} key={index}>
                <MotionCard
                  sx={{ p: 4, height: '100%', display: 'flex', flexDirection: 'column' }}
                  variants={scaleUp}
                  initial="initial"
                  whileInView="animate"
                  whileHover={{ y: -8, transition: { duration: 0.3 } }}
                  viewport={{ once: true, margin: "-100px" }}
                >
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    {item.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ flex: 1 }}>
                    {item.description}
                  </Typography>
                </MotionCard>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    </MotionBox>
  );
};

const JobSearch = () => (
  <Container maxWidth="lg" sx={{ py: 8 }}>
    <Typography 
      variant="h2" 
      sx={{ 
        mb: 6,
        fontWeight: 600,
      }}
    >
      Job Search
    </Typography>
    
    <JobSearchForm />
  </Container>
);

const ResumeBuilder = () => (
  <Container maxWidth="lg" sx={{ py: 8 }}>
    <Typography 
      variant="h2" 
      sx={{ 
        mb: 6,
        fontWeight: 600,
        color: '#000000',
      }}
    >
      Resume Builder
    </Typography>
    <Card 
      sx={{ 
        p: 4, 
        mb: 4,
        border: '1px solid #d2d2d7',
        borderRadius: 2,
      }}
    >
      <Typography 
        variant="h6" 
        sx={{ 
          mb: 2,
          color: '#000000',
        }}
      >
        Create a Standout Resume
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Here you'll be able to create and optimize your resume with AI assistance.
      </Typography>
    </Card>
  </Container>
);

const Applications = () => (
  <Container maxWidth="lg" sx={{ py: 8 }}>
    <Typography 
      variant="h2" 
      sx={{ 
        mb: 6,
        fontWeight: 600,
        color: '#000000',
      }}
    >
      Applications
    </Typography>
    <Card 
      sx={{ 
        p: 4, 
        mb: 4,
        border: '1px solid #d2d2d7',
        borderRadius: 2,
      }}
    >
      <Typography 
        variant="h6" 
        sx={{ 
          mb: 2,
          color: '#000000',
        }}
      >
        Track Your Applications
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Here you'll be able to track and manage your job applications.
      </Typography>
    </Card>
  </Container>
);

// Keyword Analysis Component
const KeywordAnalysis = () => {
  const [keywords, setKeywords] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  // Mock data for demonstration purposes
  const getMockResults = (keywordArray) => {
    // Generate enhanced keywords based on input
    const enhancedKeywords = [...keywordArray];
    
    // Add related keywords based on common patterns
    keywordArray.forEach(keyword => {
      if (keyword.toLowerCase().includes('python')) {
        enhancedKeywords.push('data science', 'machine learning', 'django', 'flask');
      } else if (keyword.toLowerCase().includes('react')) {
        enhancedKeywords.push('javascript', 'frontend', 'redux', 'web development');
      } else if (keyword.toLowerCase().includes('data')) {
        enhancedKeywords.push('analytics', 'visualization', 'sql', 'tableau');
      } else {
        // Add some generic tech keywords
        enhancedKeywords.push('agile', 'cloud computing', 'problem solving');
      }
    });
    
    // Remove duplicates and original keywords
    const uniqueEnhanced = [...new Set(enhancedKeywords)];
    
    return {
      original_keywords: keywordArray,
      enhanced_keywords: uniqueEnhanced,
      keyword_stats: {
        total_jobs_found: Math.floor(Math.random() * 5000) + 1000,
        top_paying_keywords: uniqueEnhanced.slice(0, 3),
        trending_keywords: uniqueEnhanced.slice(2, 5)
      }
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Parse keywords into array
      const keywordArray = keywords
        .split(',')
        .map(keyword => keyword.trim())
        .filter(keyword => keyword.length > 0);
      
      if (keywordArray.length === 0) {
        throw new Error('Please enter at least one keyword');
      }
      
      try {
        // Call the API
        const response = await jobDiscoveryApi.analyzeKeywords(keywordArray);
        setResults(response.data);
      } catch (apiError) {
        console.error('API Error:', apiError);
        // Use mock data if API fails
        const mockData = getMockResults(keywordArray);
        setResults(mockData);
        setError('Could not connect to the API - showing mock data for demonstration');
      }
    } catch (err) {
      console.error('Error analyzing keywords:', err);
      setError(err.message || 'An error occurred while analyzing keywords');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Typography 
        variant="h2" 
        sx={{ 
          mb: 6,
          fontWeight: 600,
        }}
      >
        Keyword Analysis
      </Typography>
      
      <Card 
        component="form"
        onSubmit={handleSubmit}
        sx={{ 
          p: 4, 
          mb: 4,
          border: '1px solid #d2d2d7',
          borderRadius: 2,
        }}
      >
        <Typography 
          variant="h6" 
          sx={{ 
            mb: 2,
          }}
        >
          Analyze Keywords
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Enter keywords to analyze and enhance them with our AI-powered system.
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={12} md={9}>
            <TextField
              label="Keywords (comma separated)"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="e.g. python, machine learning, data science"
              fullWidth
              required
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                  backgroundColor: 'rgba(0, 0, 0, 0.03)',
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button 
              variant="contained"
              type="submit"
              disabled={loading}
              fullWidth
              sx={{ 
                height: '100%',
                borderRadius: 2,
              }}
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </Button>
          </Grid>
        </Grid>
      </Card>
      
      {error && (
        <Alert severity={error.includes('mock data') ? 'warning' : 'error'} sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {results && (
        <Card 
          sx={{ 
            p: 4,
            border: '1px solid #d2d2d7',
            borderRadius: 2,
          }}
        >
          <Typography 
            variant="h6" 
            sx={{ 
              mb: 3,
            }}
          >
            Analysis Results
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Original Keywords:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
                {results.original_keywords?.map((keyword, index) => (
                  <Chip key={index} label={keyword} />
                ))}
              </Box>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Enhanced Keywords:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
                {results.enhanced_keywords?.map((keyword, index) => (
                  <Chip 
                    key={index} 
                    label={keyword} 
                    color={results.original_keywords?.includes(keyword) ? 'default' : 'primary'}
                  />
                ))}
              </Box>
            </Grid>
            
            {results.keyword_stats && (
              <>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                    Keyword Statistics:
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card sx={{ p: 2, bgcolor: 'rgba(0, 0, 0, 0.02)' }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Total Jobs Found:
                    </Typography>
                    <Typography variant="h6">
                      {results.keyword_stats.total_jobs_found?.toLocaleString() || 'N/A'}
                    </Typography>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card sx={{ p: 2, bgcolor: 'rgba(0, 0, 0, 0.02)' }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Top Paying Keywords:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {results.keyword_stats.top_paying_keywords?.map((keyword, index) => (
                        <Chip 
                          key={index} 
                          label={keyword} 
                          size="small"
                          color="success"
                        />
                      ))}
                    </Box>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card sx={{ p: 2, bgcolor: 'rgba(0, 0, 0, 0.02)' }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Trending Keywords:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {results.keyword_stats.trending_keywords?.map((keyword, index) => (
                        <Chip 
                          key={index} 
                          label={keyword} 
                          size="small"
                          color="info"
                        />
                      ))}
                    </Box>
                  </Card>
                </Grid>
              </>
            )}
          </Grid>
        </Card>
      )}
    </Container>
  );
};

// Platform Stats Component
const PlatformStats = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Call the API
        const response = await jobDiscoveryApi.getStats();
        
        // Check if response has data
        if (response && response.data) {
          setStats(response.data);
        } else {
          throw new Error('No data received from the server');
        }
      } catch (err) {
        console.error('Error fetching platform stats:', err);
        setError(err.message || 'An error occurred while fetching platform statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  // Mock data for development/testing
  const mockStats = {
    stats: {
      linkedin: {
        success_rate: 0.95,
        avg_response_time: 1.2,
        job_count: 5243,
        last_crawl_time: new Date().toISOString()
      },
      indeed: {
        success_rate: 0.88,
        avg_response_time: 1.5,
        job_count: 3127,
        last_crawl_time: new Date().toISOString()
      },
      glassdoor: {
        success_rate: 0.92,
        avg_response_time: 1.8,
        job_count: 2845,
        last_crawl_time: new Date().toISOString()
      }
    }
  };

  // Use mock data if API fails (for demo purposes)
  const displayStats = stats || mockStats;

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Typography 
        variant="h2" 
        sx={{ 
          mb: 6,
          fontWeight: 600,
        }}
      >
        Platform Statistics
      </Typography>
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <>
          <Alert severity="warning" sx={{ mb: 3 }}>
            {error} - Showing mock data for demonstration purposes.
          </Alert>
          <Grid container spacing={3}>
            {Object.entries(displayStats.stats || {}).map(([platform, platformStats]) => (
              <Grid item xs={12} md={6} lg={4} key={platform}>
                <Card 
                  sx={{ 
                    p: 4,
                    height: '100%',
                    border: '1px solid #d2d2d7',
                    borderRadius: 2,
                  }}
                >
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      mb: 2,
                      textTransform: 'capitalize',
                    }}
                  >
                    {platform}
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Success Rate:
                      </Typography>
                      <Typography variant="body1">
                        {(platformStats.success_rate * 100).toFixed(0)}%
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Response Time:
                      </Typography>
                      <Typography variant="body1">
                        {platformStats.avg_response_time.toFixed(2)}s
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Jobs Found:
                      </Typography>
                      <Typography variant="body1">
                        {platformStats.job_count}
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Last Crawl:
                      </Typography>
                      <Typography variant="body1">
                        {platformStats.last_crawl_time ? new Date(platformStats.last_crawl_time).toLocaleString() : 'Never'}
                      </Typography>
                    </Grid>
                  </Grid>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      ) : (
        <Grid container spacing={3}>
          {Object.entries(displayStats.stats || {}).map(([platform, platformStats]) => (
            <Grid item xs={12} md={6} lg={4} key={platform}>
              <Card 
                sx={{ 
                  p: 4,
                  height: '100%',
                  border: '1px solid #d2d2d7',
                  borderRadius: 2,
                }}
              >
                <Typography 
                  variant="h6" 
                  sx={{ 
                    mb: 2,
                    textTransform: 'capitalize',
                  }}
                >
                  {platform}
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Success Rate:
                    </Typography>
                    <Typography variant="body1">
                      {(platformStats.success_rate * 100).toFixed(0)}%
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Response Time:
                    </Typography>
                    <Typography variant="body1">
                      {platformStats.avg_response_time.toFixed(2)}s
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Jobs Found:
                    </Typography>
                    <Typography variant="body1">
                      {platformStats.job_count}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Last Crawl:
                    </Typography>
                    <Typography variant="body1">
                      {platformStats.last_crawl_time ? new Date(platformStats.last_crawl_time).toLocaleString() : 'Never'}
                    </Typography>
                  </Grid>
                </Grid>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

function App() {
  const location = useLocation();
  
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      bgcolor: '#ffffff', // Pure white background
      overflow: 'hidden', // Prevent horizontal scrollbar during animations
    }}>
      <Header />
      <MotionBox 
        component="main" 
        sx={{ flexGrow: 1 }}
        initial="initial"
        animate="animate"
        exit="exit"
        variants={fadeIn}
      >
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/jobs" element={<JobSearch />} />
            <Route path="/keywords" element={<KeywordAnalysis />} />
            <Route path="/stats" element={<PlatformStats />} />
            <Route path="/resume" element={<ResumeBuilder />} />
            <Route path="/applications" element={<Applications />} />
          </Routes>
        </AnimatePresence>
      </MotionBox>
      <Footer />
    </Box>
  );
}

export default App;