import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, CheckCircle, X } from 'lucide-react';
import { AnimatedBackground } from '../ui/AnimatedBackground';
import { Card3D } from '../ui/Card3D';

const inputClasses = "w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 backdrop-blur-sm";

export const ContactSection = () => {
  const [form, setForm] = useState({ name: '', email: '', company: '', message: '' });
  const [status, setStatus] = useState('idle');

  const handleSubmit = async () => {
    if (!form.name || !form.email || !form.message) {
      setStatus('error');
      return;
    }

    setStatus('loading');
    setTimeout(() => {
      setStatus('success');
      setForm({ name: '', email: '', company: '', message: '' });
      setTimeout(() => setStatus('idle'), 3000);
    }, 2000);
  };

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
    if (status === 'error') setStatus('idle');
  };

  return (
    <AnimatedBackground variant="gradient">
      <section id="contact" className="py-20">
        <div className="max-w-4xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="mb-6">
              <Bot className="h-16 w-16 text-blue-400 mx-auto" />
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              Let's Automate Together
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              Ready to transform your invoice processing with AI? Let's talk about how BillBot can help.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Card3D className="p-8 max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold text-white mb-6 text-center flex items-center justify-center">
                <Send className="mr-2 h-6 w-6 text-blue-400" />
                Send us a message
              </h3>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Full Name *</label>
                  <input
                    type="text"
                    value={form.name}
                    onChange={(e) => handleChange('name', e.target.value)}
                    className={inputClasses}
                    placeholder="John Doe"
                    disabled={status === 'loading'}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Email Address *</label>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    className={inputClasses}
                    placeholder="john@company.com"
                    disabled={status === 'loading'}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Company (Optional)</label>
                  <input
                    type="text"
                    value={form.company}
                    onChange={(e) => handleChange('company', e.target.value)}
                    className={inputClasses}
                    placeholder="Your Company"
                    disabled={status === 'loading'}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Message *</label>
                  <textarea
                    value={form.message}
                    onChange={(e) => handleChange('message', e.target.value)}
                    rows={5}
                    className={`${inputClasses} resize-none`}
                    placeholder="Tell us about your invoice processing needs..."
                    disabled={status === 'loading'}
                  />
                </div>

                <motion.button
                  onClick={handleSubmit}
                  disabled={status === 'loading'}
                  whileHover={{ scale: status === 'loading' ? 1 : 1.02 }}
                  whileTap={{ scale: status === 'loading' ? 1 : 0.98 }}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  <span className="flex items-center justify-center">
                    {status === 'loading' ? (
                      <>
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full mr-3"
                        />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Send className="mr-2 h-5 w-5" />
                        Send Message
                      </>
                    )}
                  </span>
                </motion.button>

                <AnimatePresence>
                  {status === 'success' && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="bg-green-500/20 border border-green-400/30 rounded-xl p-4 text-center"
                    >
                      <CheckCircle className="h-6 w-6 text-green-400 mx-auto mb-2" />
                      <p className="text-green-300 font-medium">Message sent successfully!</p>
                      <p className="text-green-200 text-sm">We'll get back to you within 24 hours.</p>
                    </motion.div>
                  )}

                  {status === 'error' && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="bg-red-500/20 border border-red-400/30 rounded-xl p-4 text-center"
                    >
                      <X className="h-6 w-6 text-red-400 mx-auto mb-2" />
                      <p className="text-red-300 font-medium">Please fill in all required fields</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </Card3D>
          </motion.div>
        </div>
      </section>
    </AnimatedBackground>
  );
};

export default ContactSection;
