import { Redirect, Stack } from "expo-router";
import { useUserStore } from "@/src/store/useUserStore";

import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';
import '@/global.css';

export default function RootLayout() {
  const hasUser = useUserStore((state) => state.hasUser);
  const hasProfile = useUserStore((state) => state.hasProfile);  

  return (
    
    <GluestackUIProvider mode="dark">
      <Stack screenOptions={{ headerShown: false }}>
      <Stack.Protected guard={hasUser && hasProfile}>
          <Stack.Screen name="(tabs)" />
      </Stack.Protected>
      <Stack.Screen name="(auth)" />
    </Stack>
    </GluestackUIProvider>
  
  );
}
      