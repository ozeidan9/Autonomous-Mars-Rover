import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_down(){

    try {
        fetch('http://192.168.43.50:11000/mov_ctrl', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            direction: '1538', 
        })
        });
    }catch(e){
        console.log(e);
    }
}


export default function DOWNButton(props) {
    const {title = 'Backward' } = props;
    return (
      <Pressable style={styles.button_down} onPress={() => {sendAPI_down()}}>
        <Text style={styles.text}>{title}</Text>
      </Pressable>
    );
}
      
const styles = StyleSheet.create({
   
    button_down: {
        // alignItems: 'center',
        right: 0,
        top: 190,
        paddingVertical: 20,
        paddingHorizontal: 22,
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
