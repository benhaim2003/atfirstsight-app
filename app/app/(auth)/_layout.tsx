import React, { useEffect } from 'react';
import { Stack, useRouter } from 'expo-router';
import { useUserStore } from '@/src/store/useUserStore'; 

export default function AuthLayout() {
  const hasUser = useUserStore((state) => state.hasUser);
  const hasProfile = useUserStore((state) => state.hasProfile);
  
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        presentation: 'modal',
        contentStyle: { backgroundColor: "#303133" },

      }}      
    >
      <Stack.Protected guard={!hasUser}>
        <Stack.Screen name="signUp"/>
        <Stack.Screen name="logIn"/>
      </Stack.Protected>
      <Stack.Protected guard={!hasProfile}>
        <Stack.Screen name="profileCreation"/>  
      </Stack.Protected>        
    </Stack>
  );
}