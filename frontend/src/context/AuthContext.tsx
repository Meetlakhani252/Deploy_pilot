import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  User,
  apiLogin,
  apiSignup,
  apiLogout,
  apiRefreshToken,
} from '../api/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Initialize session by attempting silent refresh on initial app load
  useEffect(() => {
    let isMounted = true;

    async function initSession() {
      try {
        const data = await apiRefreshToken();
        if (isMounted) {
          setUser(data.user);
          setToken(data.access_token);
        }
      } catch {
        // Session does not exist or refresh token expired
        if (isMounted) {
          setUser(null);
          setToken(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    initSession();

    return () => {
      isMounted = false;
    };
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const data = await apiLogin(email, password);
    setUser(data.user);
    setToken(data.access_token);
  }, []);

  const signup = useCallback(async (email: string, password: string) => {
    const data = await apiSignup(email, password);
    setUser(data.user);
    setToken(data.access_token);
  }, []);

  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } catch {
      // Clean up local state regardless of server failure
    } finally {
      setUser(null);
      setToken(null);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
