import React from 'react';
import { 
  TextField, 
  Button, 
  Checkbox, 
  FormControlLabel, 
  Radio, 
  RadioGroup,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Switch,
  Slider,
  styled,
  useTheme
} from '@mui/material';
import { motion } from 'framer-motion';

// Motion components
const MotionButton = motion(Button);

// Animation variants
const buttonVariants = {
  initial: { scale: 0.98 },
  hover: { 
    scale: 1.02,
    transition: { duration: 0.2 }
  },
  tap: { 
    scale: 0.98,
    transition: { duration: 0.1 }
  }
};

// Styled components
const StyledTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: 8,
    transition: 'all 0.2s ease',
    backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.05)',
    border: 'none',
    '&:hover': {
      backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.08)',
    },
    '&.Mui-focused': {
      backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.08)',
      boxShadow: theme.palette.mode === 'light' 
        ? '0 0 0 3px rgba(0, 0, 0, 0.1)' 
        : '0 0 0 3px rgba(255, 255, 255, 0.1)',
    },
    '& fieldset': {
      borderColor: 'transparent',
    },
    '&:hover fieldset': {
      borderColor: 'transparent',
    },
    '&.Mui-focused fieldset': {
      borderColor: 'transparent',
    },
  },
  '& .MuiInputLabel-root': {
    '&.Mui-focused': {
      color: theme.palette.text.primary,
    },
  },
  '& .MuiInputBase-input': {
    padding: '12px 16px',
  },
}));

const StyledSelect = styled(Select)(({ theme }) => ({
  borderRadius: 8,
  backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.05)',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.08)',
  },
  '&.Mui-focused': {
    backgroundColor: theme.palette.mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.08)',
    boxShadow: theme.palette.mode === 'light' 
      ? '0 0 0 3px rgba(0, 0, 0, 0.1)' 
      : '0 0 0 3px rgba(255, 255, 255, 0.1)',
  },
  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'transparent',
  },
  '&:hover .MuiOutlinedInput-notchedOutline': {
    borderColor: 'transparent',
  },
  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
    borderColor: 'transparent',
  },
  '& .MuiSelect-select': {
    padding: '12px 16px',
  },
}));

const StyledCheckbox = styled(Checkbox)(({ theme }) => ({
  color: theme.palette.text.secondary,
  '&.Mui-checked': {
    color: theme.palette.text.primary,
  },
  '& .MuiSvgIcon-root': {
    fontSize: 24,
  },
}));

const StyledRadio = styled(Radio)(({ theme }) => ({
  color: theme.palette.text.secondary,
  '&.Mui-checked': {
    color: theme.palette.text.primary,
  },
  '& .MuiSvgIcon-root': {
    fontSize: 24,
  },
}));

const StyledSlider = styled(Slider)(({ theme }) => ({
  color: theme.palette.text.primary,
  height: 4,
  '& .MuiSlider-thumb': {
    width: 20,
    height: 20,
    backgroundColor: theme.palette.background.paper,
    border: `1px solid ${theme.palette.text.primary}`,
    '&:focus, &:hover, &.Mui-active': {
      boxShadow: theme.palette.mode === 'light' 
        ? '0 0 0 8px rgba(0, 0, 0, 0.1)' 
        : '0 0 0 8px rgba(255, 255, 255, 0.1)',
    },
  },
  '& .MuiSlider-valueLabel': {
    backgroundColor: theme.palette.text.primary,
    color: theme.palette.background.paper,
    fontSize: 12,
    fontWeight: 600,
    padding: '2px 8px',
    borderRadius: 4,
  },
}));

// Apple-style form components
export const AppleTextField = (props) => {
  return <StyledTextField fullWidth {...props} />;
};

export const AppleSelect = ({ label, children, ...props }) => {
  return (
    <FormControl fullWidth>
      {label && <InputLabel>{label}</InputLabel>}
      <StyledSelect label={label} {...props}>
        {children}
      </StyledSelect>
    </FormControl>
  );
};

export const AppleCheckbox = ({ label, ...props }) => {
  return (
    <FormControlLabel
      control={<StyledCheckbox {...props} />}
      label={label}
    />
  );
};

export const AppleRadioGroup = ({ options, ...props }) => {
  return (
    <RadioGroup {...props}>
      {options.map((option) => (
        <FormControlLabel
          key={option.value}
          value={option.value}
          control={<StyledRadio />}
          label={option.label}
        />
      ))}
    </RadioGroup>
  );
};

export const AppleButton = ({ children, ...props }) => {
  return (
    <MotionButton
      variants={buttonVariants}
      initial="initial"
      whileHover="hover"
      whileTap="tap"
      {...props}
    >
      {children}
    </MotionButton>
  );
};

export const AppleSlider = (props) => {
  return <StyledSlider {...props} />;
};