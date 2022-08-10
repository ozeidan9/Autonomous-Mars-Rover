import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_4(){
 
  try {
      fetch('http://192.168.43.50:11000/start', {
      method : 'post',
      mode : 'no-cors',
      headers : {
          'Accept' : 'application/json',
          'Content-type' : 'application/json'
      },
      body : JSON.stringify({
          start: '1284', //0000010100000100
      })
      });
  }catch(e){
      console.log(e);
  }
}

export default function Start4(props) {
  const { title = '(340, 220)' } = props;
  return (
    <Pressable style={styles.button_up} onPress={()=>{sendAPI_4()}}>
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}
      
const styles = StyleSheet.create({
    button_up: {
        // alignItems: 'center',
        right: -135,
        top: 108,
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
