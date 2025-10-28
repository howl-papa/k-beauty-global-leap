import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '@/utils/api';
import { AuthState, LoginCredentials, SignupData, User, AuthResponse } from '@/types/auth';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true, error: null });
        
        try {
          // OAuth2 format: use FormData
          const formData = new FormData();
          formData.append('username', credentials.email);
          formData.append('password', credentials.password);

          const response = await api.post<AuthResponse>('/api/v1/auth/login', formData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });

          const { access_token } = response.data;

          // Store token
          localStorage.setItem('access_token', access_token);

          // Get user info
          const userResponse = await api.get<User>('/api/v1/users/me');

          set({
            user: userResponse.data,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Login failed';
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          throw error;
        }
      },

      signup: async (data: SignupData) => {
        set({ isLoading: true, error: null });
        
        try {
          // Create account
          await api.post('/api/v1/auth/signup', data);

          // Auto login after signup
          await useAuthStore.getState().login({
            email: data.email,
            password: data.password,
          });
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Signup failed';
          set({
            isLoading: false,
            error: errorMessage,
          });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem('access_token');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        });
      },

      fetchCurrentUser: async () => {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return;
        }

        set({ isLoading: true });
        
        try {
          const response = await api.get<User>('/api/v1/users/me');
          
          set({
            user: response.data,
            token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          localStorage.removeItem('access_token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
      }),
    }
  )
);
