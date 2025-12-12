import { Profile } from "@/types/profile";

export interface User {
  id: string;
  email: string;
  created_at: Date;
}

export enum UserAuthState {
    Guest = "GUEST", // No user and no profile
    User = "USER", // Has only user - no profile yet
    Member = "MEMBER" // Has profile and user registered 
}

// track the auth status of a user
export interface UserState {

    user: User | null;
    profile: Profile | null
    userAuthState: UserAuthState 

    setUser: (user: User) => void;    
    setProfile: (profile: Profile) => void;

    logout: () => void;

}