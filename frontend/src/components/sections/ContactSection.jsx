import React from 'react';
import { motion } from 'framer-motion';
import { Mail, Phone, MapPin } from 'lucide-react';
import { AnimatedBackground } from '../ui/AnimatedBackground';
import { Card3D } from '../ui/Card3D';

export const ContactSection = () => (
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
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Get In Touch
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Ready to streamline your invoice processing? Let's talk about how BillBot AI can help.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {[
            { icon: <Mail className="h-6 w-6" />, title: "Email Us", value: "hello@billbot.ai", color: "blue" },
            { icon: <Phone className="h-6 w-6" />, title: "Call Us", value: "+1 (555) 123-4567", color: "purple" },
            { icon: <MapPin className="h-6 w-6" />, title: "Find Us", value: "San Francisco, CA", color: "cyan" }
          ].map((contact, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              viewport={{ once: true }}
            >
              <Card3D className="p-6 text-center group cursor-pointer">
                <div className={`text-${contact.color}-400 mb-4`}>{contact.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{contact.title}</h3>
                <p className="text-gray-400 group-hover:text-gray-300 transition-colors">
                  {contact.value}
                </p>
              </Card3D>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  </AnimatedBackground>
);

export default ContactSection;
