import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Shield, FileText, CheckCircle } from 'lucide-react';
import { AnimatedBackground } from '../ui/AnimatedBackground';
import { Card3D } from '../ui/Card3D';

const features = [
  {
    icon: <Zap className="h-8 w-8" />,
    title: "Efficient Processing",
    description: "Process multiple invoices in seconds with our advanced AI algorithms."
  },
  {
    icon: <Shield className="h-8 w-8" />,
    title: "Secure by Design",
    description: "Your data is processed securely. Temporary files are deleted after each session."
  },
  {
    icon: <FileText className="h-8 w-8" />,
    title: "Multi-Format Support",
    description: "Handle PDFs, images (PNG, JPG), and various document formats seamlessly."
  },
  {
    icon: <CheckCircle className="h-8 w-8" />,
    title: "High Accuracy",
    description: "Leverages advanced AI models for reliable data extraction."
  }
];

export const FeaturesSection = () => (
  <AnimatedBackground variant="default">
    <section id="features" className="py-20">
      <div className="max-w-7xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Why Choose BillBot?
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Experience the future of invoice processing with features designed for modern businesses.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              viewport={{ once: true }}
            >
              <Card3D className="p-8 h-full">
                <div className="text-blue-400 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-3 text-white">{feature.title}</h3>
                <p className="text-gray-400 leading-relaxed">{feature.description}</p>
              </Card3D>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  </AnimatedBackground>
);

export default FeaturesSection;
