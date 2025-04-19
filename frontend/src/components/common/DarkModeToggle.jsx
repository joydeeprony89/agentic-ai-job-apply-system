import React from 'react';
import { IconButton, Tooltip, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import { useThemeMode } from '../../contexts/ThemeContext';

// Motion variants for icon animation
const iconVariants = {
  initial: { scale: 0.8, opacity: 0, rotate: -30 },
  animate: { 
    scale: 1, 
    opacity: 1, 
    rotate: 0,
    transition: { 
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1.0] 
    }
  },
  exit: { 
    scale: 0.8, 
    opacity: 0,
    rotate: 30,
    transition: { 
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1.0] 
    }
  },
  hover: {
    scale: 1.1,
    rotate: [0, 15, 0],
    transition: {
      rotate: {
        repeat: Infinity,
        repeatType: "mirror",
        duration: 1,
        ease: "easeInOut"
      }
    }
  },
  tap: { scale: 0.9 }
};

const MotionIconButton = motion(IconButton);

const DarkModeToggle = () => {
  const { mode, toggleColorMode } = useThemeMode();
  const theme = useTheme();
  
  return (
    <Tooltip title={mode === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}>
      <MotionIconButton
        onClick={toggleColorMode}
        aria-label={mode === 'light' ? 'dark mode' : 'light mode'}
        initial="initial"
        animate="animate"
        exit="exit"
        whileHover="hover"
        whileTap="tap"
        variants={iconVariants}
        sx={{
          color: mode === 'light' ? 'text.primary' : 'text.primary',
          ml: 1,
        }}
      >
        {mode === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
      </MotionIconButton>
    </Tooltip>
  );
};

export default DarkModeToggle;