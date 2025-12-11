import { Text, View, StyleSheet } from "react-native";
import { Link } from "expo-router";
import ImageViewer from "@/components/ImageViewer"

const PlaceHolderImage = require("../../assets/images/icon.png");

export default function Index() {
  return (
    <View style={styles.container}>
      <View style={styles.imageContainer}>
        <ImageViewer imgSource={PlaceHolderImage}/>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  imageContainer: {
    flex: 1,
  }    
});
