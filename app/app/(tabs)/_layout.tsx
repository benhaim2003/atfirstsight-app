import { Tabs } from "expo-router";

export default function TabsLayout() {
    return (
        <Tabs screenOptions={{ headerShown: false }}>
            <Tabs.Screen name="explore" options={{ title: "Explore" }} />
            <Tabs.Screen name="discover" options={{ title: "Discover" }} />
            <Tabs.Screen name="chats" options={{ title: "Chats" }} />
            <Tabs.Screen name="profile" options={{ title: "Profile" }} />
        </Tabs>
    );
}


