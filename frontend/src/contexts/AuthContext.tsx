import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, login as apiLogin, register as apiRegister, getMe, logout as apiLogout } from '../api/auth';
import { PartnershipStatus, getStatus as fetchPartnershipStatus } from '../api/partnership';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  partnership: PartnershipStatus | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  refreshPartnership: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [partnership, setPartnership] = useState<PartnershipStatus | null>(null);

  const checkAuth = async () => {
    const token = localStorage.getItem('flow_token');
    if (!token) {
      setIsLoading(false);
      return;
    }

    try {
      const userData = await getMe();
      setUser(userData);
      setIsAuthenticated(true);

      // Check partnership status
      try {
        const status = await fetchPartnershipStatus();
        setPartnership(status);
      } catch {
        setPartnership({ status: 'none' });
      }
    } catch {
      localStorage.removeItem('flow_token');
      localStorage.removeItem('flow_user');
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await apiLogin(email, password);
    setUser(response.user);
    setIsAuthenticated(true);

    // Check partnership after login
    try {
      const status = await fetchPartnershipStatus();
      setPartnership(status);
    } catch {
      setPartnership({ status: 'none' });
    }
  };

  const register = async (email: string, password: string, name: string) => {
    const response = await apiRegister(email, password, name);
    setUser(response.user);
    setIsAuthenticated(true);
    setPartnership({ status: 'none' });
  };

  const logout = () => {
    apiLogout();
    setUser(null);
    setIsAuthenticated(false);
    setPartnership(null);
  };

  const refreshPartnership = async () => {
    try {
      const status = await fetchPartnershipStatus();
      setPartnership(status);
    } catch {
      setPartnership({ status: 'none' });
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        partnership,
        login,
        register,
        logout,
        refreshPartnership,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
