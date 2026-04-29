import api from './client';

export interface PartnershipStatus {
  status: 'none' | 'pending' | 'active';
  code?: string;
  partner?: {
    id: string;
    name: string;
    email: string;
  };
  invitedAt?: string;
  joinedAt?: string;
}

export interface InviteResponse {
  code: string;
  expiresAt: string;
}

export const createInvite = async (): Promise<InviteResponse> => {
  const response = await api.post<InviteResponse>('/partnerships/invite');
  return response.data;
};

export const joinWithCode = async (code: string): Promise<PartnershipStatus> => {
  const response = await api.post<PartnershipStatus>('/partnerships/join', { code });
  return response.data;
};

export const getStatus = async (): Promise<PartnershipStatus> => {
  const response = await api.get<PartnershipStatus>('/partnerships/status');
  return response.data;
};
