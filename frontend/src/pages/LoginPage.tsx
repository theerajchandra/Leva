// /frontend/src/pages/LoginPage.tsx
import React, { useState } from 'react';
import {
  Box, Button, Input, Heading, Container, Stack, Text,
} from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';
import levaApi from '../api/levaApi';
import { useAuthStore } from '../store/authStore';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login); // Get the login action

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    try {
      const response = await levaApi.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      
      // Use the store action to save the token and update state
      login(response.data.access_token);
      
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Incorrect email or password.');
    }
    setIsLoading(false);
  };

  return (
    <Container maxW="md" py={20}>
      <Stack gap={8}>
        <Box textAlign="center">
          <Heading as="h1" size="2xl" color="blue.600">
            Leva
          </Heading>
          <Text fontSize="lg" color="gray.600" mt={2}>
            Financial OS for Freight Forwarders
          </Text>
        </Box>
        
        <Box p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
          <form onSubmit={handleSubmit}>
            <Stack gap={6}>
              <Heading as="h2" size="lg" textAlign="center">
                Login
              </Heading>
              
              {error && (
                <Box p={3} bg="red.50" borderRadius="md" color="red.600">
                  {error}
                </Box>
              )}
              
              <Box>
                <Text mb={2} fontWeight="medium">Email</Text>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="user@example.com"
                  required
                />
              </Box>
              
              <Box>
                <Text mb={2} fontWeight="medium">Password</Text>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                />
              </Box>
              
              <Button
                type="submit"
                colorScheme="blue"
                w="full"
                loading={isLoading}
              >
                Login
              </Button>
              
              <Text textAlign="center">
                Don't have an account?{' '}
                <Link to="/register" style={{ color: '#3182CE', textDecoration: 'underline' }}>
                  Register here
                </Link>
              </Text>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Container>
  );
}

export default LoginPage;
