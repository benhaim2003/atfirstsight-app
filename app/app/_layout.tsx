import { Redirect, Stack } from "expo-router";
import { UserState, UserAuthState } from "@/types/user";
import { useUserStore } from "@/src/store/useUserStore";


export default function RootLayout() {
  const userAuthState = useUserStore((state) => state.userAuthState);

  if (userAuthState === UserAuthState.Guest)
  {
    return <Redirect href="./(auth)/signIn" />;
  }

  if (userAuthState === UserAuthState.User)
  {
    return <Redirect href="./(auth)/profileCreation" />;
  }
  
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
