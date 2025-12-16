import { View, Text, StyleSheet } from 'react-native';
import { Profile } from '@/src/types/profile';

export default function ProfileCreationScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile Creation Screen</Text>
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
});