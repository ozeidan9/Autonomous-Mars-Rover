import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_3(){
 
  try {
      fetch('http://192.168.43.50:11000/start', {
      method : 'post',
      mode : 'no-cors',
      headers : {
          'Accept' : 'application/json',
          'Content-type' : 'application/json'
      },
      body : JSON.stringify({
          start: '1283', //0000010100000011
      })
      });
  }catch(e){
      console.log(e);
  }
}

export default function Start3(props) {
  const { title = '(340, 20)' } = props;
  return (
    <Pressable style={styles.button_up} onPress={()=>{sendAPI_3()}}>
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}
      
const styles = StyleSheet.create({
    button_up: {
        // alignItems: 'center',
        right: -39,
        top: 149,
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
