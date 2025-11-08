// /frontend/src/api/levaApi.ts
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const levaApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
});

// Interceptor to add the token from Zustand to every request
levaApi.interceptors.request.use(
  (config) => {
    // Get state directly from the store
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default levaApi;
