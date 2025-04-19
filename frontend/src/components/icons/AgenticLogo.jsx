import React from 'react';
import { SvgIcon } from '@mui/material';
import { motion } from 'framer-motion';

// Motion SvgIcon component
const MotionSvgIcon = motion(SvgIcon);

// Animation variants for logo
const logoVariants = {
  initial: { scale: 0.9, opacity: 0 },
  animate: { 
    scale: 1, 
    opacity: 1,
    transition: { duration: 0.4 }
  },
  hover: { 
    scale: 1.05,
    transition: { duration: 0.2 }
  },
  tap: { 
    scale: 0.95,
    transition: { duration: 0.1 }
  }
};

// Agentic AI Logo
export const AgenticLogo = (props) => (
  <MotionSvgIcon
    viewBox="0 0 36 36"
    variants={logoVariants}
    initial="initial"
    animate="animate"
    whileHover="hover"
    whileTap="tap"
    sx={{ fontSize: props.fontSize || '2rem' }}
    {...props}
  >
    {/* Brain/AI symbol with letter A integrated */}
    <path 
      d="M18,3C9.716,3,3,9.716,3,18s6.716,15,15,15s15-6.716,15-15S26.284,3,18,3z" 
      fill="currentColor" 
      opacity="0.1"
    />
    <path 
      d="M18,7l-8,20h4l1.5-4h5l1.5,4h4L18,7z M16.5,19l1.5-4l1.5,4H16.5z" 
      fill="currentColor"
    />
    <path 
      d="M26,14c0,0-2-1.5-4-1.5s-4,1.5-4,1.5v-2c0,0,2-1.5,4-1.5s4,1.5,4,1.5V14z" 
      fill="currentColor"
    />
    <path 
      d="M10,14c0,0,2-1.5,4-1.5s4,1.5,4,1.5v-2c0,0-2-1.5-4-1.5s-4,1.5-4,1.5V14z" 
      fill="currentColor"
    />
    <path 
      d="M22,18c1.105,0,2-0.895,2-2s-0.895-2-2-2s-2,0.895-2,2S20.895,18,22,18z" 
      fill="currentColor"
    />
    <path 
      d="M14,18c1.105,0,2-0.895,2-2s-0.895-2-2-2s-2,0.895-2,2S12.895,18,14,18z" 
      fill="currentColor"
    />
  </MotionSvgIcon>
);

// Simplified logo for favicon/small sizes
export const AgenticLogoSimple = (props) => (
  <MotionSvgIcon
    viewBox="0 0 36 36"
    variants={logoVariants}
    initial="initial"
    animate="animate"
    whileHover="hover"
    whileTap="tap"
    {...props}
  >
    <circle cx="18" cy="18" r="15" fill="currentColor" opacity="0.1" />
    <path 
      d="M18,7l-8,20h16L18,7z" 
      fill="currentColor"
    />
    <circle cx="14" cy="16" r="2" fill="currentColor" />
    <circle cx="22" cy="16" r="2" fill="currentColor" />
  </MotionSvgIcon>
);