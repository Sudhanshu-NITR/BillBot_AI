import React from 'react';
import { motion } from 'framer-motion';

export const Card3D = ({ children, className = "", hover = true, ...props }) => {
  return (
    <motion.div
      whileHover={hover ? {
        y: -5,
        scale: 1.02,
      } : {}}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={`
        relative bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 
        rounded-2xl shadow-lg ${className}
      `}
      {...props}
    >
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
};
