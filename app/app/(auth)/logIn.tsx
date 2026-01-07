import { useRouter } from 'expo-router';
import { useState } from 'react';
import { logIn } from '@/src/services/authServices'
import { User } from '@/src/types/user'
import { useUserStore } from '@/src/store/useUserStore';

// Gluestack UI Components
import { Input, InputField, InputIcon, InputSlot } from '@/components/ui/input';
import { FormControl } from '@/components/ui/form-control';
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Heading } from '@/components/ui/heading';
import { Text } from '@/components/ui/text';
import { Button, ButtonIcon, ButtonText } from '@/components/ui/button';
import { EyeIcon, EyeOffIcon } from '@/components/ui/icon';
import { Box } from '@/components/ui/box';
import { View } from 'react-native'; // Native View for specific dividers

export default function LogInScreen() {
  console.log("IN SCREEN OF Log In")
  
  const router = useRouter()
  const [showPassword, setShowPassword] = useState(false);
  const setUser = useUserStore((state) => state.setUser);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogIn = async () => {
    const user = await logIn(email, password);
    
    if(!user) {
      console.log("FAILED!! ==>>> Could not log in to ", email)
    }
    else {
      console.log("Log In successful - email: ", user.id)
      setUser(user);
      router.push("/profileCreation")
    }
  };

  const handleState = () => {
    setShowPassword((showState) => !showState);
  };

  return (
    // 1. Main Background Container - Dark Hex matches the image
    <Box className="flex-1 bg-[#1d1b1b] justify-center px-6">
      
      {/* Container for the form to limit max width on tablets */}
      <Box className="w-full max-w-[400px] mx-auto">

        {/* Header */}
        <VStack className="mb-10 items-center">
            <Heading className="text-white text-3xl font-bold mb-2">
                Log in to AtFirstSight
            </Heading>
        </VStack>

        <FormControl className="w-full">
          <VStack space="xl">
            
            {/* EMAIL INPUT */}
            <VStack space="xs">
              <Text className="text-gray-400 font-medium ml-1">Email</Text>
              <Input className="bg-[#262626] border-0 rounded-lg h-12">
                <InputField 
                    type="text" 
                    value={email} 
                    onChangeText={setEmail} 
                    className="placeholder:text-gray-500"
                    placeholder="name@example.com" 
                />
              </Input>
            </VStack>

            {/* PASSWORD INPUT */}
            <VStack space="xs">
              <Text className="text-gray-400 font-medium ml-1">Password</Text>
              <Input className="bg-[#262626] border-0 rounded-lg h-12">
                <InputField 
                    type={showPassword ? 'text' : 'password'} 
                    value={password} 
                    onChangeText={setPassword}
                    className="placeholder:text-gray-500"
                    placeholder="Enter your password"
                />
                <InputSlot className="pr-3" onPress={handleState}>
                  <InputIcon as={showPassword ? EyeIcon : EyeOffIcon} className="text-gray-400"/>
                </InputSlot>
              </Input>
            </VStack>

            {/* Forgot Password Link */}
            <Box className="items-end mt-[-8px]">
                 <Button variant="link" size="sm" className="p-0 h-auto">
                    <ButtonText className="text-gray-400 text-xs">Forgot your password?</ButtonText>
                 </Button>
            </Box>

            {/* LOG IN BUTTON - High Contrast White */}
            <Button 
                className="w-full bg-white rounded-full h-12 mt-2 bg-[#f07aa5]" 
                onPress={handleLogIn}
            >
              <ButtonText className="text-black font-bold text-md">Log in</ButtonText>
            </Button>

            {/* DIVIDER */}
            <HStack className="items-center my-4">
                <View className="flex-1 h-[1px] bg-gray-700" />
                <Text className="text-gray-500 mx-4 text-xs">or continue with</Text>
                <View className="flex-1 h-[1px] bg-gray-700" />
            </HStack>

            {/* SOCIAL BUTTONS */}
            <VStack space="md">
                <Button variant="outline" className="border-gray-700 rounded-lg h-12 justify-start pl-4 bg-transparent">
                    {/* Placeholder for Google Icon */}
                    <Text className="text-white font-bold mx-auto">Google</Text>
                </Button>
                <Button variant="outline" className="border-gray-700 rounded-lg h-12 justify-start pl-4 bg-transparent">
                    {/* Placeholder for Facebook Icon */}
                    <Text className="text-white font-bold mx-auto">Facebook</Text>
                </Button>
            </VStack>

            {/* SIGN UP FOOTER */}
            <HStack className="justify-center mt-6">
                <Text className="text-gray-500 text-sm">Don't have an account? </Text>
                <Button variant="link" size="sm" className="p-0 h-auto" 
                    onPress={() => router.push("/(auth)/signUp")}>
                    <ButtonText className="text-white font-bold text-sm">Sign up</ButtonText>
                </Button>
            </HStack>

          </VStack>
        </FormControl>
      </Box>
    </Box>
  );
}