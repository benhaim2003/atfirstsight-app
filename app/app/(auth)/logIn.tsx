import { useRouter } from 'expo-router';
import { View, Text, StyleSheet, TextInput, Button } from 'react-native';
import { use, useState } from 'react';
import logIn from '@/src/services/authServices'
import { User } from '@/src/types/user'
import { useUserStore } from '@/src/store/useUserStore';

export default function LogInScreen() {
  console.log("IN SCREEN OF Log In")
  
  const router = useRouter()
  const setUser = useUserStore((state) => state.setUser);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogIn = () => {
    const user: User = logIn(email, password);
    console.log("Log In successful - email: ", user.email)
    setUser(user);
    router.push("/profileCreation")
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Log In 🧭</Text>
      <Text>Email:</Text>
      <TextInput 
        placeholder="Enter your email" 
        keyboardType="email-address" 
        style={styles.input}
        value={email}
        onChangeText={setEmail}
      />
      <Text>Password:</Text>
      <TextInput 
        placeholder="Enter your password" 
        secureTextEntry 
        style={styles.input}
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Log In" onPress={handleLogIn} />
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