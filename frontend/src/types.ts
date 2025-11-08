// /frontend/src/types.ts
export interface PayablePublic {
  id: number;
  amount_due: number;
  status: string;
  carrier_name: string;
  due_date: string;
}

export interface InvoicePublic {
  id: number;
  amount: number;
  status: string;
  due_date: string;
}

export interface BookingPublic {
  id: number;
  status: string;
  client_id: number;
  reference_number: string;
  carrier_name: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  organization_id: number;
}

export interface UserPublic {
  id: number;
  email: string;
  full_name: string;
  organization_id: number;
  is_active: boolean;
}
