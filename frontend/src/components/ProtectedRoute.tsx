import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
  requirePartnership?: boolean;
}

export const ProtectedRoute = ({ children, requirePartnership = true }: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading, partnership } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="skeleton w-8 h-8 rounded-full" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requirePartnership && partnership?.status !== 'active') {
    return <Navigate to="/setup" replace />;
  }

  return <>{children}</>;
};
