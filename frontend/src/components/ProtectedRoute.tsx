'use client';

import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect, ComponentType } from 'react';

/**
 * Higher-Order Component for protecting routes
 * Wraps any component and ensures user is authenticated before rendering
 * 
 * Usage:
 * const ProtectedDashboard = withAuth(DashboardComponent);
 * 
 * Or with redirect customization:
 * const ProtectedSettings = withAuth(SettingsComponent, '/login?redirect=settings');
 */
export function withAuth<P extends object>(
  Component: ComponentType<P>,
  redirectTo: string = '/login'
) {
  return function ProtectedRoute(props: P) {
    const { isAuthenticated, isLoading } = useAuthStore();
    const router = useRouter();

    useEffect(() => {
      if (!isLoading && !isAuthenticated) {
        router.push(redirectTo);
      }
    }, [isAuthenticated, isLoading, router]);

    // Show loading spinner while checking authentication
    if (isLoading) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-pink-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 font-medium">Verifying authentication...</p>
          </div>
        </div>
      );
    }

    // Don't render anything if not authenticated
    if (!isAuthenticated) {
      return null;
    }

    // Render the protected component
    return <Component {...props} />;
  };
}

/**
 * Component wrapper for protecting page components
 * Can be used directly in page.tsx files
 * 
 * Usage:
 * export default function DashboardPage() {
 *   return (
 *     <ProtectedRoute>
 *       <YourPageContent />
 *     </ProtectedRoute>
 *   );
 * }
 */
interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
  loadingComponent?: React.ReactNode;
}

export function ProtectedRoute({ 
  children, 
  redirectTo = '/login',
  loadingComponent 
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, redirectTo, router]);

  if (isLoading) {
    return loadingComponent || (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Verifying authentication...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}

/**
 * Hook for checking authentication in components
 * Returns authentication state and utility functions
 * 
 * Usage:
 * const { requireAuth, isAuthenticated, user } = useRequireAuth();
 * 
 * useEffect(() => {
 *   requireAuth('/login');
 * }, [requireAuth]);
 */
export function useRequireAuth(redirectTo: string = '/login') {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  const router = useRouter();

  const requireAuth = (customRedirect?: string) => {
    if (!isLoading && !isAuthenticated) {
      router.push(customRedirect || redirectTo);
    }
  };

  return {
    isAuthenticated,
    isLoading,
    user,
    requireAuth,
  };
}
