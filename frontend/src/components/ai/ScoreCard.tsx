/**
 * Score Card Component
 * 
 * Displays a score with visual indicator (progress bar or circular)
 */

import React from 'react';

interface ScoreCardProps {
  title: string;
  score: number; // 0-100
  subtitle?: string;
  variant?: 'default' | 'success' | 'warning' | 'danger';
  type?: 'bar' | 'circular';
  size?: 'sm' | 'md' | 'lg';
}

const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  subtitle,
  variant = 'default',
  type = 'bar',
  size = 'md',
}) => {
  // Determine color based on score and variant
  const getColor = () => {
    if (variant !== 'default') {
      const colors = {
        success: 'bg-green-500',
        warning: 'bg-yellow-500',
        danger: 'bg-red-500',
      };
      return colors[variant];
    }

    // Auto color based on score
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getTextColor = () => {
    if (variant !== 'default') {
      const colors = {
        success: 'text-green-600',
        warning: 'text-yellow-600',
        danger: 'text-red-600',
      };
      return colors[variant];
    }

    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const sizeClasses = {
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  };

  const scoreSizeClasses = {
    sm: 'text-2xl',
    md: 'text-3xl',
    lg: 'text-4xl',
  };

  return (
    <div className={`bg-white rounded-lg shadow-md ${sizeClasses[size]}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-700">{title}</h3>
        <span className={`${scoreSizeClasses[size]} font-bold ${getTextColor()}`}>
          {Math.round(score)}
        </span>
      </div>

      {type === 'bar' && (
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full ${getColor()} transition-all duration-500`}
            style={{ width: `${score}%` }}
          />
        </div>
      )}

      {type === 'circular' && (
        <div className="flex justify-center my-4">
          <div className="relative w-24 h-24">
            <svg className="w-full h-full" viewBox="0 0 100 100">
              {/* Background circle */}
              <circle
                className="text-gray-200 stroke-current"
                strokeWidth="10"
                cx="50"
                cy="50"
                r="40"
                fill="transparent"
              />
              {/* Progress circle */}
              <circle
                className={`${getColor().replace('bg-', 'text-')} stroke-current`}
                strokeWidth="10"
                strokeLinecap="round"
                cx="50"
                cy="50"
                r="40"
                fill="transparent"
                strokeDasharray={`${2 * Math.PI * 40}`}
                strokeDashoffset={`${2 * Math.PI * 40 * (1 - score / 100)}`}
                transform="rotate(-90 50 50)"
              />
            </svg>
          </div>
        </div>
      )}

      {subtitle && <p className="text-xs text-gray-500 mt-2">{subtitle}</p>}
    </div>
  );
};

export default ScoreCard;
