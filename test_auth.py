"""
Test script to demonstrate JWT authentication.

This script:
1. Registers a new user
2. Logs in to get a JWT token
3. Uses the token to create a booking (protected endpoint)
4. Lists bookings using the token
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_auth_flow():
    print("Testing JWT Authentication Flow\n")
    print("=" * 60)
    
    # Step 1: Register a new user
    print("\n1. REGISTER NEW USER")
    print("-" * 60)
    register_data = {
        "email": "test@example.com",
        "password": "SecurePassword123",
        "full_name": "Test User",
        "organization_id": 3
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=register_data
        )
        if response.status_code == 201:
            print("SUCCESS: User registered")
            print(json.dumps(response.json(), indent=2))
        elif response.status_code == 400:
            print("User already exists, continuing with login...")
        else:
            print(f"ERROR {response.status_code}: {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Step 2: Login to get JWT token
    print("\n2. LOGIN TO GET JWT TOKEN")
    print("-" * 60)
    login_data = {
        "username": "test@example.com",  # OAuth2 uses 'username' field
        "password": "SecurePassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/token",
            data=login_data
        )
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("SUCCESS: Received JWT token")
            print(f"Token type: {token_data['token_type']}")
            print(f"Access token: {access_token[:50]}...")
        else:
            print(f"ERROR {response.status_code}: {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Step 3: Use token to access protected endpoint (create booking)
    print("\n3. CREATE BOOKING (PROTECTED ENDPOINT)")
    print("-" * 60)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    booking_data = {
        "reference_number": "BK-TEST-AUTH-001",
        "client_id": 5,
        "origin": "New York",
        "destination": "London",
        "payable_data": {
            "carrier_name": "Test Carrier",
            "amount_due": 5000.00,
            "due_date": "2024-01-31"
        },
        "invoice_data": {
            "amount": 7000.00,
            "due_date": "2024-02-28"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/bookings/",
            json=booking_data,
            headers=headers
        )
        if response.status_code == 200:
            print("SUCCESS: Booking created with authentication")
            booking = response.json()
            print(f"Booking ID: {booking['id']}")
            print(f"Reference: {booking['reference_number']}")
            print(f"Status: {booking['status']}")
        else:
            print(f"ERROR {response.status_code}: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Step 4: List bookings using token
    print("\n4. LIST BOOKINGS (PROTECTED ENDPOINT)")
    print("-" * 60)
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/bookings/",
            headers=headers
        )
        if response.status_code == 200:
            bookings = response.json()
            print(f"SUCCESS: Retrieved {len(bookings)} bookings")
            for booking in bookings[:3]:  # Show first 3
                print(f"  - {booking['reference_number']}: {booking['status']}")
        else:
            print(f"ERROR {response.status_code}: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Step 5: Try accessing without token (should fail)
    print("\n5. TEST ACCESS WITHOUT TOKEN (SHOULD FAIL)")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/bookings/")
        if response.status_code == 401:
            print("SUCCESS: Request correctly rejected without token")
            print(f"Error: {response.json()['detail']}")
        else:
            print(f"UNEXPECTED: Got status {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("Authentication test complete!\n")

if __name__ == "__main__":
    test_auth_flow()
