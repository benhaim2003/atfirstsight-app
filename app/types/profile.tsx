export enum Gender {
  Male = 'male',
  Female = 'female',
  Other = 'other',
}

export enum ProfileStatus {
  Offline = 'offline',
  Online = 'online',
}

export interface ProfilePhoto {
  id: string;
  storage_path: string;
  sort_order: number;
  uploaded_at: string; 
}

export interface Profile {
  id: string;
  username: string;
  bio: string;
  gender: Gender;
  birth_date: string; 
  status: ProfileStatus;
  photos: ProfilePhoto[];
  created_at: string; 
  updated_at: string; 
}
