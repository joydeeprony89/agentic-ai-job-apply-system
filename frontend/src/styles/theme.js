// Apple-inspired theme with light and dark modes

// Common typography settings
const typography = {
  fontFamily: [
    'SF Pro Text',
    'SF Pro Display',
    '-apple-system',
    'BlinkMacSystemFont',
    '"Helvetica Neue"',
    'Arial',
    'sans-serif',
  ].join(','),
  h1: {
    fontSize: '2.5rem',
    fontWeight: 600,
    letterSpacing: '-0.015em',
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  h6: {
    fontSize: '1.125rem',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 500,
    letterSpacing: '-0.005em',
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    letterSpacing: '-0.005em',
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    letterSpacing: '-0.005em',
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    letterSpacing: '-0.005em',
  },
  button: {
    textTransform: 'none',
    fontWeight: 500,
    letterSpacing: '-0.005em',
  },
};

// Common shape settings
const shape = {
  borderRadius: 8, // Apple uses more subtle rounded corners
};

// Light theme (default)
export const lightTheme = {
  palette: {
    mode: 'light',
    primary: {
      main: '#000000', // Pure black as primary color (Apple's main color)
      light: '#333333',
      dark: '#000000',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#000000', // Also black for secondary (true to Apple's minimalist approach)
      light: '#333333',
      dark: '#000000',
      contrastText: '#ffffff',
    },
    background: {
      default: '#ffffff', // Pure white background
      paper: '#ffffff',
      subtle: '#f5f5f7', // Apple's light gray for subtle backgrounds
    },
    text: {
      primary: '#000000', // Pure black text
      secondary: '#86868b', // Apple's subtle gray for secondary text
    },
    divider: '#d2d2d7', // Light gray dividers
    grey: {
      50: '#f5f5f7', // Apple's light gray
      100: '#e8e8ed',
      200: '#d2d2d7',
      300: '#b9b9c1',
      400: '#86868b',
      500: '#6e6e73',
      600: '#515154',
      700: '#3a3a3c',
      800: '#2c2c2e',
      900: '#1d1d1f',
    },
  },
  typography,
  shape,
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#ffffff',
          color: '#000000',
          transition: 'background-color 0.3s ease, color 0.3s ease',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 20px',
          fontWeight: 500,
          textTransform: 'none',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
        contained: {
          backgroundColor: '#000000', // Black buttons
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#333333', // Slightly lighter on hover
          },
        },
        containedPrimary: {
          backgroundColor: '#000000', // Black buttons
          '&:hover': {
            backgroundColor: '#333333', // Slightly lighter on hover
          },
        },
        outlined: {
          borderWidth: '1px',
          borderColor: '#d2d2d7', // Light gray border
          color: '#000000',
          '&:hover': {
            borderWidth: '1px',
            borderColor: '#86868b', // Darker gray on hover
            backgroundColor: 'transparent',
          },
        },
        text: {
          color: '#000000',
          '&:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          borderBottom: '1px solid #d2d2d7',
          backgroundColor: 'rgba(255, 255, 255, 0.8)', // Translucent white like Apple's navbar
          backdropFilter: 'blur(20px)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: 'none', // Apple prefers no shadows
          border: '1px solid #d2d2d7', // Light border instead
          borderRadius: 8,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            borderColor: '#d2d2d7',
            '&:hover': {
              borderColor: '#86868b',
            },
            '&.Mui-focused': {
              borderColor: '#000000',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          backgroundColor: '#f5f5f7',
          color: '#000000',
          '&.MuiChip-clickable:hover': {
            backgroundColor: '#e8e8ed',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          boxShadow: 'none',
        },
        elevation1: {
          boxShadow: 'none',
          border: '1px solid #d2d2d7',
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: '#d2d2d7', // Light gray dividers
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: {
          color: '#000000', // Black links
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'underline',
          },
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          width: 42,
          height: 26,
          padding: 0,
          '& .MuiSwitch-switchBase': {
            padding: 0,
            margin: 2,
            transitionDuration: '300ms',
            '&.Mui-checked': {
              transform: 'translateX(16px)',
              color: '#fff',
              '& + .MuiSwitch-track': {
                backgroundColor: '#000000',
                opacity: 1,
                border: 0,
              },
              '&.Mui-disabled + .MuiSwitch-track': {
                opacity: 0.5,
              },
            },
            '&.Mui-focusVisible .MuiSwitch-thumb': {
              color: '#000000',
              border: '6px solid #fff',
            },
            '&.Mui-disabled .MuiSwitch-thumb': {
              color: '#f5f5f7',
            },
            '&.Mui-disabled + .MuiSwitch-track': {
              opacity: 0.3,
            },
          },
          '& .MuiSwitch-thumb': {
            boxSizing: 'border-box',
            width: 22,
            height: 22,
          },
          '& .MuiSwitch-track': {
            borderRadius: 26 / 2,
            backgroundColor: '#d2d2d7',
            opacity: 1,
          },
        },
      },
    },
  },
};

// Dark theme
export const darkTheme = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#ffffff', // White as primary color in dark mode
      light: '#f5f5f7',
      dark: '#e8e8ed',
      contrastText: '#000000',
    },
    secondary: {
      main: '#ffffff', // Also white for secondary
      light: '#f5f5f7',
      dark: '#e8e8ed',
      contrastText: '#000000',
    },
    background: {
      default: '#000000', // Pure black background
      paper: '#1d1d1f', // Very dark gray for cards
      subtle: '#2c2c2e', // Dark gray for subtle backgrounds
    },
    text: {
      primary: '#ffffff', // White text
      secondary: '#a1a1a6', // Apple's light gray for secondary text in dark mode
    },
    divider: '#3a3a3c', // Dark gray dividers
    grey: {
      900: '#f5f5f7', // Inverted for dark mode
      800: '#e8e8ed',
      700: '#d2d2d7',
      600: '#b9b9c1',
      500: '#86868b',
      400: '#6e6e73',
      300: '#515154',
      200: '#3a3a3c',
      100: '#2c2c2e',
      50: '#1d1d1f',
    },
  },
  typography,
  shape,
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#000000',
          color: '#ffffff',
          transition: 'background-color 0.3s ease, color 0.3s ease',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 20px',
          fontWeight: 500,
          textTransform: 'none',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
        contained: {
          backgroundColor: '#ffffff', // White buttons in dark mode
          color: '#000000',
          '&:hover': {
            backgroundColor: '#e8e8ed', // Slightly darker on hover
          },
        },
        containedPrimary: {
          backgroundColor: '#ffffff', // White buttons in dark mode
          '&:hover': {
            backgroundColor: '#e8e8ed', // Slightly darker on hover
          },
        },
        outlined: {
          borderWidth: '1px',
          borderColor: '#3a3a3c', // Dark gray border
          color: '#ffffff',
          '&:hover': {
            borderWidth: '1px',
            borderColor: '#6e6e73', // Lighter gray on hover
            backgroundColor: 'transparent',
          },
        },
        text: {
          color: '#ffffff',
          '&:hover': {
            backgroundColor: 'rgba(255, 255, 255, 0.08)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          borderBottom: '1px solid #3a3a3c',
          backgroundColor: 'rgba(0, 0, 0, 0.8)', // Translucent black like Apple's dark mode navbar
          backdropFilter: 'blur(20px)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          border: '1px solid #3a3a3c', // Dark border
          borderRadius: 8,
          backgroundColor: '#1d1d1f',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            borderColor: '#3a3a3c',
            '&:hover': {
              borderColor: '#6e6e73',
            },
            '&.Mui-focused': {
              borderColor: '#ffffff',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          backgroundColor: '#2c2c2e',
          color: '#ffffff',
          '&.MuiChip-clickable:hover': {
            backgroundColor: '#3a3a3c',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          boxShadow: 'none',
          backgroundColor: '#1d1d1f',
        },
        elevation1: {
          boxShadow: 'none',
          border: '1px solid #3a3a3c',
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: '#3a3a3c', // Dark gray dividers
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: {
          color: '#ffffff', // White links in dark mode
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'underline',
          },
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          width: 42,
          height: 26,
          padding: 0,
          '& .MuiSwitch-switchBase': {
            padding: 0,
            margin: 2,
            transitionDuration: '300ms',
            '&.Mui-checked': {
              transform: 'translateX(16px)',
              color: '#000000',
              '& + .MuiSwitch-track': {
                backgroundColor: '#ffffff',
                opacity: 1,
                border: 0,
              },
              '&.Mui-disabled + .MuiSwitch-track': {
                opacity: 0.5,
              },
            },
            '&.Mui-focusVisible .MuiSwitch-thumb': {
              color: '#ffffff',
              border: '6px solid #000',
            },
            '&.Mui-disabled .MuiSwitch-thumb': {
              color: '#3a3a3c',
            },
            '&.Mui-disabled + .MuiSwitch-track': {
              opacity: 0.3,
            },
          },
          '& .MuiSwitch-thumb': {
            boxSizing: 'border-box',
            width: 22,
            height: 22,
          },
          '& .MuiSwitch-track': {
            borderRadius: 26 / 2,
            backgroundColor: '#6e6e73',
            opacity: 1,
          },
        },
      },
    },
  },
};