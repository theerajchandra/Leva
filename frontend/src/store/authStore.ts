// /frontend/src/store/authStore.ts
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  // Get initial token from localStorage (persistence)
  token: localStorage.getItem('leva_token'),
  isAuthenticated: !!localStorage.getItem('leva_token'),
  
  login: (token) => {
    localStorage.setItem('leva_token', token);
    set({ token, isAuthenticated: true });
  },
  
  logout: () => {
    localStorage.removeItem('leva_token');
    set({ token: null, isAuthenticated: false });
  },
}));
