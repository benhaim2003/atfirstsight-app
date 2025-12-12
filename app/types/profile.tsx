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
  uploaded_at: Date;
}

export interface Profile {
  id: string;
  username: string;
  bio: string;
  gender: Gender;
  birth_date: Date;
  status: ProfileStatus;
  photos: ProfilePhoto[];
  created_at: Date;
  updated_at: Date;
}
