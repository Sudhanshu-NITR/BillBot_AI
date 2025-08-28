import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Globe, Mail, Phone, MapPin } from 'lucide-react';

export const Footer = () => (
    <footer className="relative bg-slate-900/80 backdrop-blur-xl border-t border-slate-700/50 text-white py-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Main Section */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Bot className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                BillBot AI
              </span>
            </div>
            <p className="text-gray-400 mb-6 max-w-md">
              Transforming invoice processing with AI technology. 
              Fast, accurate, and secure automation for modern businesses.
            </p>
            <div className="flex space-x-4">
              {['Facebook', 'Twitter', 'LinkedIn', 'GitHub'].map((social) => (
                <motion.a
                  key={social}
                  href="#"
                  whileHover={{ scale: 1.1, y: -5 }}
                  className="w-10 h-10 bg-slate-800 border border-slate-700 rounded-full flex items-center justify-center hover:bg-blue-600 hover:border-blue-500 transition-colors"
                >
                  <Globe className="h-5 w-5 text-gray-400" />
                </motion.a>
              ))}
            </div>
          </div>
          
          {/* Product Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Product</h3>
            <ul className="space-y-2">
              {['Features', 'Pricing', 'API Docs', 'Integrations'].map((item) => (
                <li key={item}>
                  <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          
          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Contact</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-gray-500" />
                <span className="text-gray-400">hello@billbot.ai</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-gray-500" />
                <span className="text-gray-400">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-gray-500" />
                <span className="text-gray-400">177A, Bleecker Street</span>
              </div>
            </div>
          </div>

        </div>
        
        <div className="border-t border-slate-800 mt-12 pt-8 text-center">
          <p className="text-gray-500">
            © 2024 BillBot AI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
);

export default Footer;
