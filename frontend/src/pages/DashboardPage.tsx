// /frontend/src/pages/DashboardPage.tsx
import React from 'react';
import {
  Box, Button, Heading, Container, Stack, Text, Flex,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import BookingList from '../components/BookingList';

function DashboardPage() {
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box minH="100vh" bg="gray.50">
      {/* Header */}
      <Box bg="white" boxShadow="sm" py={4} px={6}>
        <Container maxW="7xl">
          <Flex justify="space-between" align="center">
            <Heading as="h1" size="lg" color="blue.600">
              Leva Dashboard
            </Heading>
            <Button colorScheme="red" variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          </Flex>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxW="7xl" py={8}>
        <Stack gap={6}>
          <Box>
            <Heading as="h2" size="md" mb={2}>
              Welcome to Leva
            </Heading>
            <Text color="gray.600">
              Financial OS for Freight Forwarders - Manage your bookings and financing below.
            </Text>
          </Box>

          {/* Bookings Section */}
          <Box bg="white" p={6} borderRadius="lg" boxShadow="sm">
            <Heading as="h3" size="md" mb={4}>
              Your Bookings
            </Heading>
            <BookingList />
          </Box>
        </Stack>
      </Container>
    </Box>
  );
}

export default DashboardPage;
