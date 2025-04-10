export interface AppealImage {
  id: number;
  image: string;
  uploaded_at: string;
}

export interface Appeal {
  id: number;
  user: number;
  category: 'electricity' | 'plumbing' | 'furniture' | 'other';
  description: string;
  image_base64?: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
  images: AppealImage[];
}

export interface AppealForm {
  category: Appeal['category'];
  description: string;
  image_base64?: string;
}

export interface AppealUpdate {
  status: Appeal['status'];
  comment?: string;
} 