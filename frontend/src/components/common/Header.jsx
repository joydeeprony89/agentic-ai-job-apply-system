import React, { useState, useEffect } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box, 
  Container,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import DarkModeToggle from './DarkModeToggle';
import { useThemeMode } from '../../contexts/ThemeContext';
import { 
  DashboardIcon, 
  JobSearchIcon, 
  ResumeIcon, 
  ApplicationIcon 
} from '../icons/AppleIcons';
import { AgenticLogo } from '../icons/AgenticLogo';

const Header = () => {
  const theme = useTheme();
  const { mode } = useThemeMode();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: DashboardIcon },
    { name: 'Jobs', path: '/jobs', icon: JobSearchIcon },
    { name: 'Keywords', path: '/keywords', icon: ResumeIcon },
    { name: 'Stats', path: '/stats', icon: ApplicationIcon },
    { name: 'Resume', path: '/resume', icon: ResumeIcon },
    { name: 'Applications', path: '/applications', icon: ApplicationIcon }
  ];

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 2 }}>
        <AgenticLogo sx={{ mr: 1, color: 'text.primary' }} />
        <Typography variant="h6" sx={{ fontWeight: 600, color: 'text.primary' }}>
          Agentic AI
        </Typography>
      </Box>
      <List>
        {navItems.map((item) => (
          <ListItem 
            key={item.name} 
            component={RouterLink} 
            to={item.path}
            selected={location.pathname === item.path}
            sx={{ 
              color: 'text.primary',
              '&.Mui-selected': {
                backgroundColor: 'transparent',
                color: 'text.primary',
                fontWeight: 600,
              }
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: 'text.primary' }}>
              <item.icon fontSize="small" />
            </ListItemIcon>
            <ListItemText 
              primary={item.name} 
              primaryTypographyProps={{ 
                sx: { 
                  fontWeight: location.pathname === item.path ? 600 : 400,
                  color: 'text.primary',
                }
              }}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <AppBar 
      position="sticky" 
      color="default" 
      elevation={0}
      sx={{ 
        backgroundColor: mode === 'light' 
          ? (scrolled ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 255, 255, 0.95)')
          : (scrolled ? 'rgba(0, 0, 0, 0.8)' : 'rgba(0, 0, 0, 0.95)'),
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid',
        borderColor: mode === 'light' ? '#d2d2d7' : '#3a3a3c',
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ height: 44 }}> {/* Apple's navbar is 44px tall */}
          <Box
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <AgenticLogo sx={{ mr: 1, color: 'text.primary' }} />
            <Typography
              variant="h6"
              sx={{
                fontWeight: 600,
                letterSpacing: '-0.01em',
                color: 'text.primary',
                fontSize: '1.25rem',
              }}
            >
              Agentic AI
            </Typography>
          </Box>

          {isMobile ? (
            <IconButton
              aria-label="open drawer"
              edge="end"
              onClick={handleDrawerToggle}
              sx={{ color: '#000000' }}
            >
              <MenuIcon />
            </IconButton>
          ) : (
            <Box sx={{ display: 'flex', gap: 4, alignItems: 'center' }}>
              {navItems.map((item) => (
                <Button
                  key={item.name}
                  component={RouterLink}
                  to={item.path}
                  startIcon={<item.icon />}
                  sx={{
                    color: 'text.primary',
                    fontWeight: location.pathname === item.path ? 600 : 400,
                    fontSize: '0.875rem',
                    minWidth: 'auto',
                    padding: '8px 8px',
                    '&:hover': {
                      backgroundColor: 'transparent',
                      opacity: 0.7,
                    },
                  }}
                >
                  {item.name}
                </Button>
              ))}
              <DarkModeToggle />
            </Box>
          )}
        </Toolbar>
      </Container>

      <Drawer
        anchor="right"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 240,
            backgroundColor: '#ffffff', // Pure white background
          },
        }}
      >
        {drawer}
      </Drawer>
    </AppBar>
  );
};

export default Header;