import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Globe } from 'lucide-react';
import { AnimatedBackground } from '../ui/AnimatedBackground';

export const Footer = () => (
  <AnimatedBackground variant="dark">
    <footer className="py-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center">
          <motion.div 
            className="flex items-center justify-center space-x-2 mb-4"
            whileHover={{ scale: 1.05 }}
          >
            <Bot className="h-8 w-8 text-blue-400" />
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              BillBot AI
            </span>
          </motion.div>
          <p className="text-gray-400 mb-6 max-w-md mx-auto">
            Automating invoice processing with AI. Fast, accurate, and secure.
          </p>
        </div>
        
        <motion.div 
          className="border-t border-slate-800 mt-12 pt-8 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p className="text-gray-500">
            © 2024 BillBot AI. All rights reserved.
          </p>
        </motion.div>
      </div>
    </footer>
  </AnimatedBackground>
);

export default Footer;
