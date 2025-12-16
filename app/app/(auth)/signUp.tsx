import { useRouter } from 'expo-router';
import { View, Text, StyleSheet, TextInput, Button, Alert } from 'react-native';
import { useState } from 'react';
import { signUp } from '@/src/services/authServices'
import { User } from '@/src/types/user'
import { useUserStore } from '@/src/store/useUserStore';

export default function SignUpScreen() {
  console.log("IN SCREEN OF SIGN UP")
  
  const router = useRouter()
  const setUser = useUserStore((state) => state.setUser);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignUp = () => {
    if (password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    
    const user: User = signUp(email, password);
    console.log("Sign up successful - email: ", user.email)
    setUser(user);
    router.push("/(auth)/profileCreation")
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign Up 📝</Text>
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
      <Text>Confirm Password:</Text>
      <TextInput 
        placeholder="Confirm your password" 
        secureTextEntry 
        style={styles.input}
        value={confirmPassword}
        onChangeText={setConfirmPassword}
      />
      <Button title="Sign Up" onPress={handleSignUp} />
      <Button 
        title="Already have an account? Log In" 
        onPress={() => router.push("/(auth)/logIn")}
      />
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
