import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  MenuItem,
  Divider,
  Stack
} from '@mui/material';
import { motion } from 'framer-motion';
import { 
  AppleTextField, 
  AppleSelect, 
  AppleCheckbox, 
  AppleRadioGroup, 
  AppleButton,
  AppleSlider
} from '../common/AppleFormElements';
import { fadeIn, slideUp } from '../../utils/transitions';

// Motion components
const MotionBox = motion(Box);
const MotionCard = motion(Card);

const JobSearchForm = () => {
  // Form state
  const [formData, setFormData] = useState({
    jobTitle: '',
    location: '',
    jobType: '',
    experienceLevel: '',
    salary: [50000, 150000],
    remoteOnly: false,
    notificationPreference: 'email',
  });

  // Handle form changes
  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: e.target.type === 'checkbox' ? checked : value
    }));
  };

  // Handle slider change
  const handleSliderChange = (event, newValue) => {
    setFormData(prev => ({
      ...prev,
      salary: newValue
    }));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Add form submission logic here
  };

  return (
    <MotionBox
      component="form"
      onSubmit={handleSubmit}
      variants={fadeIn}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <Typography 
        variant="h4" 
        sx={{ 
          mb: 4,
          fontWeight: 600,
        }}
      >
        Find Your Perfect Job
      </Typography>

      <MotionCard
        variants={slideUp}
        sx={{ 
          p: 4, 
          mb: 4,
        }}
      >
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography 
              variant="h6" 
              sx={{ 
                mb: 3,
                fontWeight: 600,
              }}
            >
              Job Preferences
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleTextField
              label="Job Title"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="e.g. Software Engineer, Product Manager"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleTextField
              label="Location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. San Francisco, Remote"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleSelect
              label="Job Type"
              name="jobType"
              value={formData.jobType}
              onChange={handleChange}
            >
              <MenuItem value="">Select Job Type</MenuItem>
              <MenuItem value="full-time">Full-time</MenuItem>
              <MenuItem value="part-time">Part-time</MenuItem>
              <MenuItem value="contract">Contract</MenuItem>
              <MenuItem value="internship">Internship</MenuItem>
            </AppleSelect>
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleSelect
              label="Experience Level"
              name="experienceLevel"
              value={formData.experienceLevel}
              onChange={handleChange}
            >
              <MenuItem value="">Select Experience Level</MenuItem>
              <MenuItem value="entry">Entry Level</MenuItem>
              <MenuItem value="mid">Mid Level</MenuItem>
              <MenuItem value="senior">Senior Level</MenuItem>
              <MenuItem value="executive">Executive</MenuItem>
            </AppleSelect>
          </Grid>

          <Grid item xs={12}>
            <Typography 
              variant="subtitle1" 
              gutterBottom
              sx={{ fontWeight: 500, mt: 2 }}
            >
              Salary Range: ${formData.salary[0].toLocaleString()} - ${formData.salary[1].toLocaleString()}
            </Typography>
            <AppleSlider
              value={formData.salary}
              onChange={handleSliderChange}
              min={0}
              max={300000}
              step={5000}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `$${value.toLocaleString()}`}
            />
          </Grid>

          <Grid item xs={12}>
            <AppleCheckbox
              label="Remote Only"
              name="remoteOnly"
              checked={formData.remoteOnly}
              onChange={handleChange}
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 4 }} />

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography 
              variant="h6" 
              sx={{ 
                mb: 3,
                fontWeight: 600,
              }}
            >
              Notification Preferences
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <AppleRadioGroup
              name="notificationPreference"
              value={formData.notificationPreference}
              onChange={handleChange}
              options={[
                { value: 'email', label: 'Email Notifications' },
                { value: 'sms', label: 'SMS Notifications' },
                { value: 'both', label: 'Both Email and SMS' },
                { value: 'none', label: 'No Notifications' },
              ]}
            />
          </Grid>
        </Grid>

        <Stack 
          direction={{ xs: 'column', sm: 'row' }} 
          spacing={2} 
          justifyContent="flex-end"
          sx={{ mt: 4 }}
        >
          <AppleButton 
            variant="outlined"
            type="reset"
            onClick={() => setFormData({
              jobTitle: '',
              location: '',
              jobType: '',
              experienceLevel: '',
              salary: [50000, 150000],
              remoteOnly: false,
              notificationPreference: 'email',
            })}
          >
            Reset
          </AppleButton>
          <AppleButton 
            variant="contained"
            type="submit"
          >
            Search Jobs
          </AppleButton>
        </Stack>
      </MotionCard>
    </MotionBox>
  );
};

export default JobSearchForm;