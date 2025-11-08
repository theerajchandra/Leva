// /frontend/src/pages/RegisterPage.tsx
import React, { useState } from 'react';
import {
  Box, Button, Input, Heading, Container, Stack, Text,
} from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';
import levaApi from '../api/levaApi';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [organizationName, setOrganizationName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess(false);

    try {
      await levaApi.post('/auth/register', {
        email,
        password,
        full_name: fullName,
        organization_name: organizationName,
      });
      
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
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
                Register
              </Heading>
              
              {error && (
                <Box p={3} bg="red.50" borderRadius="md" color="red.600">
                  {error}
                </Box>
              )}
              
              {success && (
                <Box p={3} bg="green.50" borderRadius="md" color="green.600">
                  Registration successful! Redirecting to login...
                </Box>
              )}
              
              <Box>
                <Text mb={2} fontWeight="medium">Organization Name</Text>
                <Input
                  type="text"
                  value={organizationName}
                  onChange={(e) => setOrganizationName(e.target.value)}
                  placeholder="Your Company Name"
                  required
                />
              </Box>
              
              <Box>
                <Text mb={2} fontWeight="medium">Full Name</Text>
                <Input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="John Doe"
                  required
                />
              </Box>
              
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
                Register
              </Button>
              
              <Text textAlign="center">
                Already have an account?{' '}
                <Link to="/login" style={{ color: '#3182CE', textDecoration: 'underline' }}>
                  Login here
                </Link>
              </Text>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Container>
  );
}

export default RegisterPage;
