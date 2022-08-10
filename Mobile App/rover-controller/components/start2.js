import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_2(){
 
  try {
      fetch('http://192.168.43.50:11000/start', {
      method : 'post',
      mode : 'no-cors',
      headers : {
          'Accept' : 'application/json',
          'Content-type' : 'application/json'
      },
      body : JSON.stringify({
          start: '1282', 
                  
      })
      });
  }catch(e){
      console.log(e);
  }
}

export default function Start2(props) {
  const { title = '(20, 220)' } = props;
  return (
    <Pressable style={styles.button_up} onPress={()=>{sendAPI_2()}}>
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}
      
const styles = StyleSheet.create({
    button_up: {
        // alignItems: 'center',
        right: 53,
        top: 189,
        paddingVertical: 10,
        paddingHorizontal: 5,
        borderRadius: 10,
        elevation: 3,
        backgroundColor: '#036',
    },

    text: {
        fontSize: 16,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
        color: 'white',
    },
});
