import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Upload, ArrowRight, Clock, CheckCircle, X, Sparkles, Info, Copy, Check } from 'lucide-react';

// Reusable UI Components
import { AnimatedBackground } from '../ui/AnimatedBackground.jsx';
import { Card3D } from '../ui/Card3D.jsx';

// A small, self-contained component for the loading animation
const LoadingAnimation = () => (
  <div className="flex items-center justify-center space-x-2">
    <div className="flex space-x-1">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{
            scale: [1, 1.4, 1],
            opacity: [0.7, 1, 0.7],
            backgroundColor: ['#3b82f6', '#8b5cf6', '#06b6d4', '#3b82f6']
          }}
          transition={{
            duration: 1.2,
            repeat: Infinity,
            delay: i * 0.2
          }}
          className="w-3 h-3 rounded-full"
        />
      ))}
    </div>
    <span className="ml-2">Processing...</span>
  </div>
);


export const BotInteractionSection = ({ driveLink, setDriveLink, status, setStatus, errorMessage, setErrorMessage }) => {
  const [copied, setCopied] = useState(false);
  const serviceAccountEmail = "billbot-ai-service@billbot-ai.iam.gserviceaccount.com";

  const handleCopy = () => {
    navigator.clipboard.writeText(serviceAccountEmail);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
  };
  
  const handleSubmit = async () => {
    if (!driveLink.trim() || !driveLink.startsWith("https://drive.google.com/")) {
      setStatus('error');
      setErrorMessage('Please enter a valid Google Drive folder link.');
      return;
    }

    setStatus('loading');
    setErrorMessage('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/process-invoices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ drive_link: driveLink }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'Invoices_Processed.xlsx';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        setStatus('success');
      } else {
        const errorData = await response.json();
        setStatus('error');
        setErrorMessage(errorData.error || 'An unexpected server error occurred.');
      }
    } catch (error) {
      setStatus('error');
      setErrorMessage('Network error. Please check your connection or the server status.');
    }
  };

  return (
    <AnimatedBackground variant="gradient">
      <section id="bot-section" className="py-20">
        <div className="max-w-4xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Card3D className="p-8 md:p-12" hover={false}>
              <div className="text-center mb-8">
                  <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-white">
                    Meet Your AI Assistant
                  </h2>
                  <p className="text-center text-gray-400 mb-8 text-lg">
                    Drop your Google Drive link and let the AI work its magic ✨
                  </p>
              </div>

              {/* Input Section */}
              <motion.div 
                className="space-y-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                viewport={{ once: true }}
              >
                <div className="relative">
                  <Upload className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500 h-5 w-5 z-10" />
                  <motion.input
                    whileFocus={{ scale: 1.02, borderColor: '#3b82f6' }}
                    type="url"
                    value={driveLink}
                    onChange={(e) => setDriveLink(e.target.value)}
                    placeholder="Paste your Google Drive folder link here..."
                    className="w-full pl-12 pr-4 py-4 bg-slate-900/50 border border-slate-600 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent backdrop-blur-sm transition-all duration-300"
                    disabled={status === 'loading'}
                  />
                </div>

                {/* --- NEW: User Instructions --- */}
                <motion.div 
                  className="bg-slate-800/60 border border-slate-700 p-4 rounded-lg text-sm text-slate-300 flex items-start space-x-3"
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  viewport={{ once: true }}
                >
                  <Info className="h-5 w-5 text-blue-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-bold mb-2">Important: Grant Access</p>
                    <p className="mb-2">For the bot to read your files, please share your Google Drive folder with our service account:</p>
                    <div className="flex items-center justify-between bg-slate-900 p-2 rounded-md">
                      <code className="text-cyan-400 text-xs break-all">{serviceAccountEmail}</code>
                      <button onClick={handleCopy} className="ml-2 p-1 rounded-md hover:bg-slate-700 transition-colors">
                        {copied ? <Check className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4 text-slate-400" />}
                      </button>
                    </div>
                  </div>
                </motion.div>
                
                <motion.button
                  onClick={handleSubmit}
                  disabled={status === 'loading'}
                  whileHover={{ scale: status === 'loading' ? 1 : 1.02 }}
                  whileTap={{ scale: status === 'loading' ? 1 : 0.98 }}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-4 px-8 rounded-2xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  {status === 'loading' ? <LoadingAnimation /> : (
                    <span className="flex items-center justify-center">
                      <Sparkles className="mr-2 h-5 w-5" />
                      Process My Invoices
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </span>
                  )}
                </motion.button>
              </motion.div>

              {/* Status Display */}
              <AnimatePresence>
                {status !== 'idle' && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="mt-8"
                  >
                    {status === 'loading' && (
                      <Card3D className="p-6 text-center bg-blue-500/10 border-blue-400/30">
                        <Clock className="h-8 w-8 mx-auto text-blue-400 mb-3" />
                        <p className="text-white font-semibold text-lg mb-2">AI Processing in Progress</p>
                        <p className="text-blue-300">Analyzing your invoices... please wait.</p>
                      </Card3D>
                    )}
                    {status === 'success' && (
                      <Card3D className="p-6 text-center bg-green-500/10 border-green-400/30">
                        <CheckCircle className="h-12 w-12 text-green-400 mx-auto mb-3" />
                        <p className="text-white font-semibold text-lg mb-2">🎉 Success!</p>
                        <p className="text-green-300">Your Excel report is downloading now.</p>
                      </Card3D>
                    )}
                    {status === 'error' && (
                      <Card3D className="p-6 text-center bg-red-500/10 border-red-400/30">
                        <X className="h-8 w-8 text-red-400 mx-auto mb-3" />
                        <p className="text-white font-semibold text-lg mb-2">Processing Error</p>
                        <p className="text-red-300">{errorMessage}</p>
                      </Card3D>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </Card3D>
          </motion.div>
        </div>
      </section>
    </AnimatedBackground>
  );
};

export default BotInteractionSection;
