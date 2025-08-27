import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle } from 'lucide-react';
import { AnimatedBackground } from '../ui/AnimatedBackground';
import { Card3D } from '../ui/Card3D';

export const AboutSection = () => (
  <AnimatedBackground variant="dark">
    <section id="about" className="py-20">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              About BillBot AI
            </h2>
            <p className="text-lg text-gray-400 mb-6 leading-relaxed">
              We're simplifying how businesses handle invoice processing. Our AI technology eliminates manual data entry, reduces errors, and saves valuable time.
            </p>
            <p className="text-lg text-gray-400 mb-8 leading-relaxed">
              Built by a team of AI and automation experts, BillBot AI is trusted by companies to streamline their financial workflows.
            </p>
            <div className="grid grid-cols-3 gap-8">
              {[
                { value: "1000s", label: "Invoices Processed", color: "text-blue-400" },
                { value: "50+", label: "Happy Clients", color: "text-purple-400" },
                { value: "98%", label: "Accuracy Rate", color: "text-cyan-400" }
              ].map((stat, index) => (
                <motion.div 
                  key={index}
                  className="text-center"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.6 }}
                  viewport={{ once: true }}
                >
                  <div className={`text-3xl font-bold ${stat.color} mb-2`}>{stat.value}</div>
                  <div className="text-gray-500">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Card3D className="p-8 bg-gradient-to-br from-slate-800/80 to-slate-900/80">
              <h3 className="text-2xl font-bold mb-6 text-white">Why Businesses Love Us</h3>
              <div className="space-y-4">
                {[
                  "Save 90% of manual processing time",
                  "Reduce human errors to near zero",
                  "Process any format: PDF, JPG, PNG",
                  "Enterprise-grade security & compliance",
                  "Real-time processing and notifications"
                ].map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.6 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <CheckCircle className="h-5 w-5 text-green-400" />
                    <span className="text-gray-300">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </Card3D>
          </motion.div>
        </div>
      </div>
    </section>
  </AnimatedBackground>
);

export default AboutSection;
