// /frontend/src/components/BookingList.tsx
import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box, Button, Stack, Text, Badge, Grid, Spinner, Flex,
} from '@chakra-ui/react';
import levaApi from '../api/levaApi';
import type { BookingPublic } from '../types';

function BookingList() {
  const queryClient = useQueryClient();

  // Fetch bookings with React Query
  const { data: bookings, isLoading, error } = useQuery({
    queryKey: ['bookings'],
    queryFn: async () => {
      const response = await levaApi.get<BookingPublic[]>('/bookings/');
      return response.data;
    },
  });

  // Mutation for requesting financing
  const requestFinancingMutation = useMutation({
    mutationFn: async (bookingId: number) => {
      const response = await levaApi.post(`/finance/financing-requests/`, {
        booking_id: bookingId,
        requested_amount: 0, // This would come from a form in a real app
        advance_percentage: 80,
      });
      return response.data;
    },
    onSuccess: () => {
      // Invalidate bookings query to refetch updated data
      queryClient.invalidateQueries({ queryKey: ['bookings'] });
    },
  });

  const handleRequestFinancing = (bookingId: number) => {
    if (window.confirm('Request financing for this booking?')) {
      requestFinancingMutation.mutate(bookingId);
    }
  };

  // Status badge color mapping
  const getStatusColor = (status: string) => {
    const statusColors: { [key: string]: string } = {
      'booked': 'blue',
      'in_transit': 'purple',
      'delivered': 'green',
      'cancelled': 'red',
    };
    return statusColors[status] || 'gray';
  };

  if (isLoading) {
    return (
      <Flex justify="center" py={8}>
        <Spinner size="xl" color="blue.500" />
      </Flex>
    );
  }

  if (error) {
    return (
      <Box p={4} bg="red.50" borderRadius="md" color="red.600">
        Error loading bookings: {(error as Error).message}
      </Box>
    );
  }

  if (!bookings || bookings.length === 0) {
    return (
      <Box p={8} textAlign="center" color="gray.500">
        <Text>No bookings found. Create your first booking to get started.</Text>
      </Box>
    );
  }

  return (
    <Stack gap={4}>
      {bookings.map((booking) => (
        <Box
          key={booking.id}
          p={5}
          borderWidth={1}
          borderRadius="md"
          bg="gray.50"
          _hover={{ boxShadow: 'md', bg: 'white' }}
          transition="all 0.2s"
        >
          <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                Reference Number
              </Text>
              <Text fontWeight="bold">{booking.reference_number}</Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                Carrier
              </Text>
              <Text fontWeight="medium">{booking.carrier_name}</Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                Client ID
              </Text>
              <Text fontWeight="medium">{booking.client_id}</Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                Status
              </Text>
              <Badge colorScheme={getStatusColor(booking.status)}>
                {booking.status.replace('_', ' ').toUpperCase()}
              </Badge>
            </Box>

            <Box display="flex" alignItems="flex-end">
              <Button
                size="sm"
                colorScheme="blue"
                onClick={() => handleRequestFinancing(booking.id)}
                loading={requestFinancingMutation.isPending}
              >
                Request Financing
              </Button>
            </Box>
          </Grid>
        </Box>
      ))}
    </Stack>
  );
}

export default BookingList;
