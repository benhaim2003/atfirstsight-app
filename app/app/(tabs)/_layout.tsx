import { Tabs } from "expo-router";

export default function TabsLayout() {
  return (
        <Tabs>
            <Tabs.Screen
            name="index"
            options={{
                headerTitle: "index",
            }}
            />    
            <Tabs.Screen
            name="explore"
            options={{
                headerTitle: "Explore",
            }}
            />        
        </Tabs>
    );
}


