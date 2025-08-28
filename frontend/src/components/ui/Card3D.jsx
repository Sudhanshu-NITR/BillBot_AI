import React from 'react';
import { motion } from 'framer-motion';

export const Card3D = ({ children, className = "", hover = true, variant = "default", ...props }) => {
  const variants = {
    default: "bg-slate-800/50 backdrop-blur-xl border border-slate-700/50",
    gradient: "bg-gradient-to-br from-slate-800/90 via-slate-700/80 to-slate-900/90 backdrop-blur-xl border border-slate-600/30",
    glass: "bg-white/5 backdrop-blur-xl border border-white/10",
    highlight: "bg-gradient-to-br from-blue-900/20 via-slate-800/80 to-purple-900/20 backdrop-blur-xl border border-blue-500/20"
  };

  return (
    <motion.div
      whileHover={hover ? {
        y: -8,
        scale: 1.02,
        rotateX: 2,
        rotateY: 2,
      } : {}}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      className={`
        relative ${variants[variant]} rounded-2xl shadow-2xl 
        hover:shadow-blue-500/10 transition-shadow duration-300
        ${className}
      `}
      style={{
        transformStyle: 'preserve-3d',
      }}
      {...props}
    >
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-transparent to-purple-500/5 rounded-2xl" />
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
};
