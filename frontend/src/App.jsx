import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { Box, Container, Typography, Card, Grid, Button, Stack, Divider } from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

// Import layout components
import Header from './components/common/Header';
import Footer from './components/common/Footer';

// Import animations
import { fadeIn, slideUp, staggerContainer, scaleUp } from './utils/transitions';

// Import global styles
import './styles/global.css';
// Import the JobSearchForm
import JobSearchForm from './components/forms/JobSearchForm';
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