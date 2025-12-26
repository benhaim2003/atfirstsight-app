import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserState, User } from '@/src/types/user'
import { Profile } from '@/src/types/profile';

export const useUserStore = create<UserState>()(
    //persist(
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

            deleteUser: () => set({
                user: null,
                hasUser: false
            }),
            
            deleteProfile: () => set({
                profile: null,
                hasProfile: false 
            }),
            
            logout: () => set({
                user: null,
                profile: null,
                hasUser: false,
                hasProfile: false
            })
        }),
        // {
        //     name: 'user-store',
        //     storage: createJSONStorage(() => AsyncStorage),
        // }
    //)
);
