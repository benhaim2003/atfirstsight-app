import { useRouter } from 'expo-router';
import { View, Text, StyleSheet, TextInput, Button } from 'react-native';
import { use, useState } from 'react';
import signIn from '@/src/services/authServices'
import { User } from '@/src/types/user'
import { useUserStore } from '@/src/store/useUserStore';

export default function SignInScreen() {
  console.log("IN SCREEN OF SIGN IN")
  
  const router = useRouter()
  const setUser = useUserStore((state) => state.setUser);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = () => {
    const user: User = signIn(email, password);
    console.log("Sign in successful - email: ", user.email)
    setUser(user);
    router.push("/(auth)/profileCreation")
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign In 🧭</Text>
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
      <Button title="Sign In" onPress={handleSignIn} />
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