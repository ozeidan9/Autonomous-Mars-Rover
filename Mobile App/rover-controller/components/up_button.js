import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_up(){
 
  try {
      fetch('http://192.168.43.50:11000/mov_ctrl', {
      method : 'post',
      mode : 'no-cors',
      headers : {
          'Accept' : 'application/json',
          'Content-type' : 'application/json'
      },
      body : JSON.stringify({
          direction: '1537', //
      })
      });
  }catch(e){
      console.log(e);
  }
}

export default function UPButton(props) {
  const { title = 'Forward' } = props;
  return (
    <Pressable style={styles.button_up} onPress={()=>{sendAPI_up()}}>
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
}
      
const styles = StyleSheet.create({
    button_up: {
        // alignItems: 'center',
        right: 0,
        top: 65,
        paddingVertical: 20,
        paddingHorizontal: 26,
        borderRadius: 10,
        elevation: 3,
        backgroundColor: '#740F35',
    },

    text: {
        fontSize: 16,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
        color: 'white',
    },
});
