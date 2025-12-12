import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserState, UserAuthState, User } from '@/types/user'
import { Profile } from '@/types/profile';

export const useUserStore = create<UserState>()(
    persist(
        (set, get) => ({
            user: null, 
            profile: null,
            userAuthState: UserAuthState.Guest,
                        
            setUser: (userData: User | null ) => {
                const currentProfile = get().profile;
                const newState = calculateAuthState(userData, currentProfile);

                set({ 
                    user: userData, 
                    userAuthState: newState 
                });
            },
                

            setProfile: (profileData: Profile | null) => {
                const currentUser = get().user;
                const newState = calculateAuthState(currentUser, profileData);

                set({ 
                    profile: profileData, 
                    userAuthState: newState 
                });
            },
            
            setAuthState: (newState: UserAuthState) => set({ userAuthState: newState }),

            logout: () => set({ 
                user: null, 
                profile: null, 
                userAuthState: UserAuthState.Guest 
            }),
        
        }),
        {
            name: 'atfirstsight-storage',
            storage: createJSONStorage(() => AsyncStorage),
        }
    )
);


const calculateAuthState = (user: any, profile: any): UserAuthState => {
    if (!user && profile) {
        console.error("ERROR - Created Profile without a user")
        return UserAuthState.Guest; // Force registration again
        
    }

    if (!user && !profile) {
        return UserAuthState.Guest; 
    }

    if (user && !profile) {
        return UserAuthState.User;      
    }

    return UserAuthState.Member;
};

