import React, { useState, useEffect } from 'react';

// Layout Components
import Navigation from './components/layout/Navigation';
import MobileMenu from './components/layout/MobileMenu';
import Footer from './components/layout/Footer';

// Section Components
import HeroSection from './components/sections/HeroSection';
import FeaturesSection from './components/sections/FeaturesSection';
import BotInteractionSection from './components/sections/BotInteractionSection';
import AboutSection from './components/sections/AboutSection';
import ContactSection from './components/sections/ContactSection';

function App() {
  const [driveLink, setDriveLink] = useState('');
  const [status, setStatus] = useState('idle'); // 'idle', 'loading', 'success', 'error'
  const [errorMessage, setErrorMessage] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Prevent background scroll when the mobile menu is open
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isMenuOpen]);

  return (
    <div className="min-h-screen bg-slate-900 text-white overflow-x-hidden">
      <Navigation isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />
      <MobileMenu isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />
      
      <main>
        <HeroSection />
        <FeaturesSection />
        <BotInteractionSection 
          driveLink={driveLink}
          setDriveLink={setDriveLink}
          status={status}
          setStatus={setStatus}
          errorMessage={errorMessage}
          setErrorMessage={setErrorMessage}
        />
        <AboutSection />
        <ContactSection />
      </main>
      
      <Footer />
    </div>
  );
}

export default App;
