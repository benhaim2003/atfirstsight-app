import { View, Text, StyleSheet, TextInput, Button } from 'react-native';
import { useState } from 'react';
import { useRouter } from 'expo-router';
import { Profile, ProfileStatus } from '@/src/types/profile';
import { useUserStore } from '@/src/store/useUserStore';

export default function ProfileCreationScreen() {  
  const router = useRouter();
  const userId = useUserStore((state) => state.user?.id);
  const setProfile = useUserStore((state) => state.setProfile);
  const [username, setUsername] = useState('');
  const [bio, setBio] = useState('');

  const handleCreateProfile = () => {
    if (!userId) {
      console.log("No user found");
      return;
    }

    const profile: Profile = {
      id: userId,
      username,
      bio,
      gender: 'other' as any,
      birth_date: new Date(),
      status: ProfileStatus.Online,
      photos: [],
      created_at: new Date(),
      updated_at: new Date(),
    };

    console.log("Profile created: ", profile);
    setProfile(profile);
    router.push("/(tabs)/explore");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Your Profile</Text>
      
      <Text>Username:</Text>
      <TextInput 
        placeholder="Enter your username" 
        style={styles.input}
        value={username}
        onChangeText={setUsername}
      />
      
      <Text>Bio:</Text>
      <TextInput 
        placeholder="Tell us about yourself" 
        style={styles.input}
        value={bio}
        onChangeText={setBio}
        multiline
      />
      
      <Button title="Create Profile" onPress={handleCreateProfile} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 8,
    width: '100%',
  },
});