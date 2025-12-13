import { Stack } from "expo-router";
import { UserState, UserAuthState } from "@/types/user";
import { useUserStore } from "@/src/store/useUserStore";


export default function RootLayout() {
  const userAuthState = useUserStore((state) => state.userAuthState);
  
  return (
      <Stack>
        <Stack.Screen
          name="(tabs)"
          options={{
            headerTitle: "Main Title",}}
        />
      </Stack>
  );
}
