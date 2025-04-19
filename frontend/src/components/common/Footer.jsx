import React from 'react';
import { Box, Typography, Container, Grid, Link, Divider } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Footer = () => {
  return (
    <Box 
      component="footer" 
      sx={{ 
        py: 4, 
        mt: 'auto', 
        backgroundColor: '#f5f5f7', // Apple's light gray background
        borderTop: '1px solid',
        borderColor: '#d2d2d7' // Apple's light gray border
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography 
              variant="subtitle1" 
              sx={{ 
                fontWeight: 600, 
                mb: 2,
                color: '#000000' // Pure black text
              }}
            >
              Agentic AI
            </Typography>
            <Typography 
              variant="body2" 
              color="#86868b" // Apple's secondary text color
              sx={{ mb: 2, maxWidth: 300 }}
            >
              Intelligent job application system powered by agentic AI technology.
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={2}>
            <Typography 
              variant="subtitle2" 
              sx={{ 
                fontWeight: 600, 
                mb: 2,
                color: '#000000' // Pure black text
              }}
            >
              Features
            </Typography>
            <Box component="ul" sx={{ p: 0, m: 0, listStyle: 'none' }}>
              {['Job Discovery', 'Resume Analysis', 'Application Generator'].map((item) => (
                <Box component="li" key={item} sx={{ mb: 1 }}>
                  <Link 
                    component={RouterLink} 
                    to="/" 
                    underline="hover"
                    sx={{ 
                      color: '#86868b', // Apple's secondary text color
                      fontSize: '0.75rem',
                      '&:hover': {
                        color: '#000000' // Pure black on hover
                      }
                    }}
                  >
                    {item}
                  </Link>
                </Box>
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12} sm={6} md={2}>
            <Typography 
              variant="subtitle2" 
              sx={{ 
                fontWeight: 600, 
                mb: 2,
                color: '#000000' // Pure black text
              }}
            >
              Resources
            </Typography>
            <Box component="ul" sx={{ p: 0, m: 0, listStyle: 'none' }}>
              {['Documentation', 'API', 'Support'].map((item) => (
                <Box component="li" key={item} sx={{ mb: 1 }}>
                  <Link 
                    component={RouterLink} 
                    to="/" 
                    underline="hover"
                    sx={{ 
                      color: '#86868b', // Apple's secondary text color
                      fontSize: '0.75rem',
                      '&:hover': {
                        color: '#000000' // Pure black on hover
                      }
                    }}
                  >
                    {item}
                  </Link>
                </Box>
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12} sm={6} md={2}>
            <Typography 
              variant="subtitle2" 
              sx={{ 
                fontWeight: 600, 
                mb: 2,
                color: '#000000' // Pure black text
              }}
            >
              Company
            </Typography>
            <Box component="ul" sx={{ p: 0, m: 0, listStyle: 'none' }}>
              {['About', 'Privacy', 'Terms'].map((item) => (
                <Box component="li" key={item} sx={{ mb: 1 }}>
                  <Link 
                    component={RouterLink} 
                    to="/" 
                    underline="hover"
                    sx={{ 
                      color: '#86868b', // Apple's secondary text color
                      fontSize: '0.75rem',
                      '&:hover': {
                        color: '#000000' // Pure black on hover
                      }
                    }}
                  >
                    {item}
                  </Link>
                </Box>
              ))}
            </Box>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 3, borderColor: '#d2d2d7' }} />
        
        <Box sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', sm: 'row' }, 
          justifyContent: 'space-between', 
          alignItems: { xs: 'flex-start', sm: 'center' },
          py: 1
        }}>
          <Typography variant="body2" color="#86868b" sx={{ mb: { xs: 1, sm: 0 }, fontSize: '0.7rem' }}>
            © {new Date().getFullYear()} Agentic AI. All rights reserved.
          </Typography>
          <Box sx={{ display: 'flex', gap: 3 }}>
            <Link 
              href="#" 
              underline="hover"
              sx={{ 
                color: '#86868b', // Apple's secondary text color
                fontSize: '0.7rem',
                '&:hover': {
                  color: '#000000' // Pure black on hover
                }
              }}
            >
              Privacy Policy
            </Link>
            <Link 
              href="#" 
              underline="hover"
              sx={{ 
                color: '#86868b', // Apple's secondary text color
                fontSize: '0.7rem',
                '&:hover': {
                  color: '#000000' // Pure black on hover
                }
              }}
            >
              Terms of Use
            </Link>
            <Link 
              href="#" 
              underline="hover"
              sx={{ 
                color: '#86868b', // Apple's secondary text color
                fontSize: '0.7rem',
                '&:hover': {
                  color: '#000000' // Pure black on hover
                }
              }}
            >
              Legal
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;