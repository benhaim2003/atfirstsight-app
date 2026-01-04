import { Profile } from "@/src/types/profile";

export interface User {
  id: string;
  email: string;
  created_at: Date;
}

export interface UserState {

    user: User | null;
    profile: Profile | null
    hasUser: boolean;
    hasProfile: boolean;

    setUser: (user: User) => void;    
    setProfile: (profile: Profile) => void;
    deleteUser: () => void;
    deleteProfile: () => void;

    logout: () => void;

}