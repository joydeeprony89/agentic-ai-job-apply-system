import React, { createContext, useState, useContext, useMemo, useEffect } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles';
import { lightTheme, darkTheme } from '../styles/theme';

// Create context
const ThemeContext = createContext({
  mode: 'light',
  toggleColorMode: () => {},
});

// Custom hook to use the theme context
export const useThemeMode = () => useContext(ThemeContext);

// Theme provider component
export const ThemeProvider = ({ children }) => {
  // Check if user has a preference stored in localStorage
  const storedMode = localStorage.getItem('themeMode');
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // Initialize state with stored preference, system preference, or default to light
  const [mode, setMode] = useState(storedMode || (prefersDarkMode ? 'dark' : 'light'));

  // Create the theme object based on current mode
  const theme = useMemo(
    () => createTheme(mode === 'light' ? lightTheme : darkTheme),
    [mode]
  );

  // Toggle between light and dark modes
  const toggleColorMode = () => {
    setMode((prevMode) => {
      const newMode = prevMode === 'light' ? 'dark' : 'light';
      localStorage.setItem('themeMode', newMode);
      return newMode;
    });
  };

  // Listen for system preference changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      if (!localStorage.getItem('themeMode')) {
        setMode(e.matches ? 'dark' : 'light');
      }
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  // Context value
  const contextValue = useMemo(
    () => ({
      mode,
      toggleColorMode,
    }),
    [mode]
  );

  return (
    <ThemeContext.Provider value={contextValue}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};