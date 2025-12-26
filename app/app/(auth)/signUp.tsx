import { useRouter } from 'expo-router';
import { useState } from 'react';
import { Alert, View } from 'react-native'; // Keep Alert for validation
import { signUp } from '@/src/services/authServices';
import { User } from '@/src/types/user';
import { useUserStore } from '@/src/store/useUserStore';

// Gluestack UI Imports (Consistent with Login)
import { Input, InputField, InputIcon, InputSlot } from '@/components/ui/input';
import { FormControl } from '@/components/ui/form-control';
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Heading } from '@/components/ui/heading';
import { Text } from '@/components/ui/text';
import { Button, ButtonText } from '@/components/ui/button';
import { EyeIcon, EyeOffIcon } from '@/components/ui/icon';
import { Box } from '@/components/ui/box';

export default function SignUpScreen() {
  console.log("IN SCREEN OF SIGN UP");
  
  const router = useRouter();
  const setUser = useUserStore((state) => state.setUser);
  
  // State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  // Visibility Toggles
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleSignUp = () => {
    // Basic Client-Side Validation
    if (!email || !password || !confirmPassword) {
        Alert.alert('Missing Info', 'Please fill in all fields.');
        return;
    }

    if (password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    
    // Attempt Sign Up
    const user: User | null = signUp(email, password); // Assuming signUp returns null on fail based on previous logic pattern
    
    if (user) {
        console.log("Sign up successful - email: ", user.email);
        setUser(user);
        router.push("/(auth)/profileCreation");
    } else {
        // Handle mock error
        Alert.alert('Error', 'Could not create account.');
    }
  };

  return (
    // 1. Background - Deep Charcoal #121212
    <Box className="flex-1 bg-[#121212] justify-center px-6">
      
      <Box className="w-full max-w-[400px] mx-auto">
        
        {/* Header */}
        <VStack className="mb-8">
            <Heading className="text-white text-3xl font-bold mb-1">
                Create account
            </Heading>
            <Text className="text-gray-400 text-sm">
                Join the movement. Real connections only.
            </Text>
        </VStack>

        <FormControl className="w-full">
          <VStack space="xl">
            
            {/* EMAIL */}
            <VStack space="xs">
              <Text className="text-gray-400 font-medium ml-1">Email</Text>
              <Input className="bg-[#262626] border-0 rounded-lg h-12">
                <InputField 
                    type="text" 
                    value={email} 
                    onChangeText={setEmail} 
                    className="text-white placeholder:text-gray-500"
                    placeholder="name@example.com"
                    keyboardType="email-address"
                    autoCapitalize="none"
                />
              </Input>
            </VStack>

            {/* PASSWORD */}
            <VStack space="xs">
              <Text className="text-gray-400 font-medium ml-1">Password</Text>
              <Input className="bg-[#262626] border-0 rounded-lg h-12">
                <InputField 
                    type={showPassword ? 'text' : 'password'} 
                    value={password} 
                    onChangeText={setPassword}
                    className="text-white placeholder:text-gray-500"
                    placeholder="Create a password"
                />
                <InputSlot className="pr-3" onPress={() => setShowPassword(!showPassword)}>
                  <InputIcon as={showPassword ? EyeIcon : EyeOffIcon} className="text-gray-400"/>
                </InputSlot>
              </Input>
            </VStack>

            {/* CONFIRM PASSWORD */}
            <VStack space="xs">
              <Text className="text-gray-400 font-medium ml-1">Confirm Password</Text>
              <Input className="bg-[#262626] border-0 rounded-lg h-12">
                <InputField 
                    type={showConfirmPassword ? 'text' : 'password'} 
                    value={confirmPassword} 
                    onChangeText={setConfirmPassword}
                    className="text-white placeholder:text-gray-500"
                    placeholder="Re-enter password"
                />
                <InputSlot className="pr-3" onPress={() => setShowConfirmPassword(!showConfirmPassword)}>
                  <InputIcon as={showConfirmPassword ? EyeIcon : EyeOffIcon} className="text-gray-400"/>
                </InputSlot>
              </Input>
            </VStack>

            {/* SIGN UP BUTTON */}
            <Button 
                className="w-full bg-white rounded-full h-12 mt-4" 
                onPress={handleSignUp}
            >
              <ButtonText className="text-black font-bold text-md">Sign Up</ButtonText>
            </Button>

            {/* LOGIN LINK */}
            <HStack className="justify-center mt-6">
                <Text className="text-gray-500 text-sm">Already have an account? </Text>
                <Button variant="link" size="sm" className="p-0 h-auto" onPress={() => router.push("/(auth)/logIn")}>
                    <ButtonText className="text-white font-bold text-sm">Log in</ButtonText>
                </Button>
            </HStack>

          </VStack>
        </FormControl>
      </Box>
    </Box>
  );
}