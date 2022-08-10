import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


  export default function Title() {
    
    return (
        <Text style={styles.text}>Mars Rover</Text>
    );
  }


  const styles = StyleSheet.create({
   
  
      text: {
          fontSize: 30,
          alignContent: 'center',
          position: 'absolute',
          fontWeight: 'bold',
          letterSpacing: 0.25,
          color: 'white',
          top: 70
      },
  });
  


