import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserState, UserAuthState, User } from '@/src/types/user'
import { Profile } from '@/src/types/profile';

export const useUserStore = create<UserState>()(
    (set) => ({
        user: null, 
        profile: null,
        hasUser: false,
        hasProfile: false,
                    
        setUser: (userData: User) => {
            set({ 
                user: userData, 
                hasUser: true
            });
        },

        setProfile: (profileData: Profile) => {
            set({ 
                profile: profileData, 
                hasProfile: true 
            });
        },
        
        logout: () => set({ 
            user: null, 
            profile: null, 
            hasUser: false,
            hasProfile: false
        })
    }),
);
