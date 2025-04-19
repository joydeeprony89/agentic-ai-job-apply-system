import React from 'react';
import { Box, Typography, Grid, useTheme, useMediaQuery } from '@mui/material';
import { motion, useScroll, useTransform } from 'framer-motion';

// Motion components
const MotionBox = motion(Box);
const MotionTypography = motion(Typography);

// Hero image with parallax effect
export const ParallaxHeroImage = ({ 
  src, 
  alt, 
  height = { xs: 300, md: 500, lg: 600 },
  overlayText,
  overlaySubtext,
  darkOverlay = true
}) => {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, 150]);
  
  return (
    <Box 
      sx={{ 
        position: 'relative', 
        height, 
        width: '100%', 
        overflow: 'hidden',
        borderRadius: 2,
      }}
    >
      <MotionBox
        component="img"
        src={src}
        alt={alt}
        style={{ y }}
        sx={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: 'center',
          display: 'block',
        }}
      />
      
      {(overlayText || overlaySubtext) && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: darkOverlay ? 'rgba(0, 0, 0, 0.4)' : 'rgba(255, 255, 255, 0.2)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: 4,
            textAlign: 'center',
          }}
        >
          {overlayText && (
            <MotionTypography
              variant="h2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              sx={{
                color: darkOverlay ? 'white' : 'text.primary',
                fontWeight: 600,
                mb: 2,
                textShadow: darkOverlay ? '0 2px 4px rgba(0,0,0,0.5)' : 'none',
              }}
            >
              {overlayText}
            </MotionTypography>
          )}
          
          {overlaySubtext && (
            <MotionTypography
              variant="h5"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              sx={{
                color: darkOverlay ? 'white' : 'text.primary',
                maxWidth: 700,
                textShadow: darkOverlay ? '0 1px 2px rgba(0,0,0,0.5)' : 'none',
              }}
            >
              {overlaySubtext}
            </MotionTypography>
          )}
        </Box>
      )}
    </Box>
  );
};

// Apple-style grid layout for images
export const AppleImageGrid = ({ images }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  if (!images || images.length === 0) return null;
  
  // Different layouts based on number of images
  if (images.length === 1) {
    return (
      <MotionBox
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        sx={{ borderRadius: 2, overflow: 'hidden' }}
      >
        <Box
          component="img"
          src={images[0].src}
          alt={images[0].alt}
          sx={{
            width: '100%',
            height: { xs: 300, md: 500 },
            objectFit: 'cover',
            display: 'block',
          }}
        />
      </MotionBox>
    );
  }
  
  if (images.length === 2) {
    return (
      <Grid container spacing={2}>
        {images.map((image, index) => (
          <Grid item xs={12} md={6} key={index}>
            <MotionBox
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              sx={{ borderRadius: 2, overflow: 'hidden', height: '100%' }}
            >
              <Box
                component="img"
                src={image.src}
                alt={image.alt}
                sx={{
                  width: '100%',
                  height: { xs: 250, md: 400 },
                  objectFit: 'cover',
                  display: 'block',
                }}
              />
            </MotionBox>
          </Grid>
        ))}
      </Grid>
    );
  }
  
  // 3 or more images
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={8}>
        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ borderRadius: 2, overflow: 'hidden' }}
        >
          <Box
            component="img"
            src={images[0].src}
            alt={images[0].alt}
            sx={{
              width: '100%',
              height: { xs: 300, md: 500 },
              objectFit: 'cover',
              display: 'block',
            }}
          />
        </MotionBox>
      </Grid>
      
      <Grid item xs={12} md={4}>
        <Grid container spacing={2} direction={isMobile ? 'row' : 'column'}>
          {images.slice(1, 3).map((image, index) => (
            <Grid item xs={6} md={12} key={index} sx={{ height: isMobile ? 'auto' : '50%' }}>
              <MotionBox
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: (index + 1) * 0.1 }}
                sx={{ borderRadius: 2, overflow: 'hidden', height: '100%' }}
              >
                <Box
                  component="img"
                  src={image.src}
                  alt={image.alt}
                  sx={{
                    width: '100%',
                    height: { xs: 150, md: '100%' },
                    objectFit: 'cover',
                    display: 'block',
                  }}
                />
              </MotionBox>
            </Grid>
          ))}
        </Grid>
      </Grid>
      
      {images.length > 3 && (
        <Grid item xs={12}>
          <Grid container spacing={2}>
            {images.slice(3, 7).map((image, index) => (
              <Grid item xs={6} sm={6} md={3} key={index + 3}>
                <MotionBox
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: (index + 3) * 0.1 }}
                  sx={{ borderRadius: 2, overflow: 'hidden' }}
                >
                  <Box
                    component="img"
                    src={image.src}
                    alt={image.alt}
                    sx={{
                      width: '100%',
                      height: 200,
                      objectFit: 'cover',
                      display: 'block',
                    }}
                  />
                </MotionBox>
              </Grid>
            ))}
          </Grid>
        </Grid>
      )}
    </Grid>
  );
};

// Apple-style product showcase with image and text side by side
export const ProductShowcase = ({ 
  imageSrc, 
  imageAlt, 
  title, 
  description, 
  imageOnRight = false,
  darkBackground = false
}) => {
  const theme = useTheme();
  
  return (
    <Box 
      sx={{ 
        py: { xs: 6, md: 10 },
        backgroundColor: darkBackground 
          ? theme.palette.mode === 'dark' ? 'background.paper' : '#000000'
          : theme.palette.mode === 'dark' ? 'background.default' : '#ffffff',
      }}
    >
      <Grid 
        container 
        spacing={4} 
        alignItems="center" 
        direction={imageOnRight ? { xs: 'column-reverse', md: 'row' } : { xs: 'column-reverse', md: 'row-reverse' }}
      >
        <Grid item xs={12} md={6}>
          <MotionBox
            initial={{ opacity: 0, x: imageOnRight ? -50 : 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            sx={{ p: { xs: 2, md: 6 } }}
          >
            <MotionTypography
              variant="h3"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              sx={{ 
                mb: 3,
                fontWeight: 600,
                color: darkBackground && !theme.palette.mode === 'dark' ? 'white' : 'text.primary',
              }}
            >
              {title}
            </MotionTypography>
            
            <MotionTypography
              variant="body1"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.3 }}
              sx={{ 
                mb: 4,
                color: darkBackground && !theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.8)' : 'text.secondary',
                fontSize: '1.1rem',
                lineHeight: 1.6,
              }}
            >
              {description}
            </MotionTypography>
          </MotionBox>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <MotionBox
            initial={{ opacity: 0, x: imageOnRight ? 50 : -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            sx={{ 
              borderRadius: 2, 
              overflow: 'hidden',
              boxShadow: darkBackground ? 'none' : theme.palette.mode === 'dark' ? 'none' : '0 20px 40px rgba(0,0,0,0.1)',
            }}
          >
            <Box
              component="img"
              src={imageSrc}
              alt={imageAlt}
              sx={{
                width: '100%',
                height: 'auto',
                display: 'block',
              }}
            />
          </MotionBox>
        </Grid>
      </Grid>
    </Box>
  );
};