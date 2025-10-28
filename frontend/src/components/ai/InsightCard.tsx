/**
 * Insight Card Component
 * 
 * Displays AI-generated insights with icons and badges
 */

import React from 'react';

interface InsightCardProps {
  title: string;
  insights: string[] | { [key: string]: any };
  icon?: React.ReactNode;
  variant?: 'info' | 'success' | 'warning' | 'danger';
  collapsible?: boolean;
}

const InsightCard: React.FC<InsightCardProps> = ({
  title,
  insights,
  icon,
  variant = 'info',
  collapsible = false,
}) => {
  const [isExpanded, setIsExpanded] = React.useState(!collapsible);

  const variantClasses = {
    info: 'border-blue-200 bg-blue-50',
    success: 'border-green-200 bg-green-50',
    warning: 'border-yellow-200 bg-yellow-50',
    danger: 'border-red-200 bg-red-50',
  };

  const iconColors = {
    info: 'text-blue-600',
    success: 'text-green-600',
    warning: 'text-yellow-600',
    danger: 'text-red-600',
  };

  const renderInsights = () => {
    if (Array.isArray(insights)) {
      return (
        <ul className="space-y-2">
          {insights.map((insight, index) => (
            <li key={index} className="flex items-start">
              <svg
                className="w-5 h-5 mr-2 mt-0.5 text-gray-600 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-sm text-gray-700">{insight}</span>
            </li>
          ))}
        </ul>
      );
    }

    // Render object insights
    return (
      <div className="space-y-3">
        {Object.entries(insights).map(([key, value]) => (
          <div key={key}>
            <h4 className="text-sm font-semibold text-gray-700 mb-1 capitalize">
              {key.replace(/_/g, ' ')}
            </h4>
            {Array.isArray(value) ? (
              <ul className="pl-4 space-y-1">
                {value.map((item, idx) => (
                  <li key={idx} className="text-sm text-gray-600">
                    • {typeof item === 'string' ? item : JSON.stringify(item)}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-600">{String(value)}</p>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className={`border-2 rounded-lg p-4 ${variantClasses[variant]}`}>
      <div
        className={`flex items-center justify-between ${collapsible ? 'cursor-pointer' : ''}`}
        onClick={() => collapsible && setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center space-x-3">
          {icon && <div className={iconColors[variant]}>{icon}</div>}
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        </div>
        {collapsible && (
          <svg
            className={`w-5 h-5 text-gray-500 transform transition-transform ${
              isExpanded ? 'rotate-180' : ''
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        )}
      </div>

      {isExpanded && <div className="mt-4">{renderInsights()}</div>}
    </div>
  );
};

export default InsightCard;
