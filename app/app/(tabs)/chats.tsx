import { View, Text, StyleSheet } from 'react-native';

export default function ChatListScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chat List 💬</Text>
      <Text>Only verified, in-person meetings unlock this chat.</Text>
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