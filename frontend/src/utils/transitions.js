// Apple-inspired animation utilities

// Page transition - fade in
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { 
    opacity: 1,
    transition: { 
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1.0] // Apple's cubic-bezier easing
    }
  },
  exit: { 
    opacity: 0,
    transition: { 
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  }
};

// Slide up transition (for elements entering from bottom)
export const slideUp = {
  initial: { y: 20, opacity: 0 },
  animate: { 
    y: 0, 
    opacity: 1,
    transition: { 
      duration: 0.6,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  },
  exit: { 
    y: 10, 
    opacity: 0,
    transition: { 
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  }
};

// Staggered children animation
export const staggerContainer = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

// Scale animation for cards and buttons
export const scaleUp = {
  initial: { scale: 0.98, opacity: 0 },
  animate: { 
    scale: 1, 
    opacity: 1,
    transition: { 
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  },
  hover: { 
    scale: 1.02,
    transition: { 
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  },
  tap: { 
    scale: 0.98,
    transition: { 
      duration: 0.1,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  }
};

// Apple's spring animation for interactive elements
export const springTransition = {
  type: "spring",
  stiffness: 300,
  damping: 30
};

// Subtle rotation for hover effects
export const subtleRotate = {
  initial: { rotate: 0 },
  hover: { 
    rotate: 1,
    transition: { 
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1.0]
    }
  }
};

// Parallax scroll effect
export const parallaxScroll = (yOffset) => ({
  initial: { y: 0 },
  animate: {
    y: yOffset,
    transition: {
      type: 'tween',
      ease: 'linear',
      duration: 0.1
    }
  }
});