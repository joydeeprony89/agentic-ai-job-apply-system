import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  MenuItem,
  Divider,
  Stack,
  Alert,
  CircularProgress
} from '@mui/material';
import { motion } from 'framer-motion';
import { 
  AppleTextField, 
  AppleSelect, 
  AppleCheckbox, 
  AppleRadioGroup, 
  AppleButton,
  AppleSlider,
  AppleMultiSelect
} from '../common/AppleFormElements';
import { fadeIn, slideUp } from '../../utils/transitions';
import { jobDiscoveryApi } from '../../services/api';

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
    salary: [500000, 2000000], // Salary in INR
    platforms: [], // Selected platforms
    remoteOnly: false,
    notificationPreference: 'email',
  });

  // API state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchResults, setSearchResults] = useState(null);

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
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    
    // Reset states
    setError(null);
    setSearchResults(null);
    setLoading(true);
    
    try {
      // Extract keywords from job title
      const keywords = formData.jobTitle
        .split(/[ ,]+/)
        .filter(keyword => keyword.length > 0);
      
      if (keywords.length === 0) {
        throw new Error('Please enter at least one keyword in the job title field');
      }
      
      // Call the API
      const response = await jobDiscoveryApi.searchJobs(
        keywords, 
        formData.location,
        {
          platforms: formData.platforms.length > 0 ? formData.platforms : undefined,
          salary_range: formData.salary,
          job_type: formData.jobType || undefined,
          experience_level: formData.experienceLevel || undefined,
          remote_only: formData.remoteOnly || undefined
        }
      );
      setSearchResults(response.data);
      console.log('API response:', response.data);
    } catch (err) {
      console.error('Error searching for jobs:', err);
      setError(err.message || 'An error occurred while searching for jobs');
    } finally {
      setLoading(false);
    }
  };

  return (
    <MotionBox
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
        component="form"
        onSubmit={handleSubmit}
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
              label="Job Title / Keywords"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="e.g. Software Engineer, Python, React"
              required
              helperText="Enter job title or keywords separated by spaces or commas"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleTextField
              label="Location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. San Francisco, Remote"
              required
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
              Salary Range (INR): ₹{formData.salary[0].toLocaleString()} - ₹{formData.salary[1].toLocaleString()}
            </Typography>
            <AppleSlider
              value={formData.salary}
              onChange={handleSliderChange}
              min={300000}
              max={5000000}
              step={100000}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `₹${value.toLocaleString()}`}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <AppleMultiSelect
              label="Platforms"
              name="platforms"
              value={formData.platforms}
              onChange={handleChange}
              options={[
                { value: 'LinkedIn', label: 'LinkedIn' },
                { value: 'Naukri', label: 'Naukri' },
                { value: 'Indeed', label: 'Indeed' },
                { value: 'Glassdoor', label: 'Glassdoor' }
              ]}
            />
          </Grid>

          <Grid item xs={12} md={6}>
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
            onClick={() => {
              setFormData({
                jobTitle: '',
                location: '',
                jobType: '',
                experienceLevel: '',
                salary: [500000, 2000000],
                platforms: [],
                remoteOnly: false,
                notificationPreference: 'email',
              });
              setSearchResults(null);
              setError(null);
            }}
            disabled={loading}
          >
            Reset
          </AppleButton>
          <AppleButton 
            variant="contained"
            type="submit"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : null}
          >
            {loading ? 'Searching...' : 'Search Jobs'}
          </AppleButton>
        </Stack>
      </MotionCard>

      {/* Error message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Search results */}
      {searchResults && (
        <MotionCard
          variants={slideUp}
          sx={{ p: 4 }}
        >
          <Typography 
            variant="h5" 
            sx={{ 
              mb: 3,
              fontWeight: 600,
            }}
          >
            Search Results ({searchResults.count || 0} jobs found)
          </Typography>

          {searchResults.count > 0 ? (
            <Grid container spacing={3}>
              {searchResults.jobs.map((job, index) => (
                <Grid item xs={12} key={index}>
                  <Card sx={{ p: 3, border: '1px solid #d2d2d7', borderRadius: 2 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                      {job.title}
                    </Typography>
                    <Typography variant="subtitle1" sx={{ mb: 2 }}>
                      {job.company} • {job.location}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 2 }}>
                      {job.description?.substring(0, 200)}...
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="caption" color="text.secondary">
                        {job.platform} • Posted: {job.date_posted || 'Unknown'}
                      </Typography>
                      <AppleButton 
                        variant="contained" 
                        size="small"
                        href={job.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View Job
                      </AppleButton>
                    </Box>
                  </Card>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Alert severity="info">
              No jobs found matching your criteria. Try broadening your search.
            </Alert>
          )}
        </MotionCard>
      )}
    </MotionBox>
  );
};

export default JobSearchForm;