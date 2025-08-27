import React from 'react';
import { motion } from 'framer-motion';

export const AnimatedBackground = ({ children, variant = 'default' }) => {
  const particles = Array.from({ length: 30 }, (_, i) => i);
  
  const backgroundVariants = {
    default: "from-slate-900 via-purple-900/20 to-slate-900",
    hero: "from-slate-900 via-blue-900/30 to-purple-900/20",
    dark: "from-gray-900 via-slate-900 to-black",
    gradient: "from-purple-900/40 via-slate-900 to-blue-900/40"
  };
  
  return (
    <div className={`relative overflow-hidden ${backgroundVariants[variant]}`}>
      {/* Floating Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {particles.map((i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-blue-400/30 rounded-full"
            animate={{
              x: [0, Math.random() * 200 - 100],
              y: [0, Math.random() * 200 - 100],
              opacity: [0, 1, 0],
              scale: [0, 1, 0]
            }}
            transition={{
              duration: Math.random() * 15 + 10,
              repeat: Infinity,
              ease: "linear",
              delay: Math.random() * 5
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};
