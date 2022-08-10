import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_left(){
 
    try {
        fetch('http://192.168.43.50:11000/mov_ctrl', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            direction: '1539', //0000100000000011
                    
        })
        });
    }catch(e){
        console.log(e);
    }
}

export default function LEFTButton(props) {
    const { title = 'Left' } = props;
    return (
        <Pressable style={styles.button_left} onPress={()=>{sendAPI_left()}}>
        <Text style={styles.text}>{title}</Text>
        </Pressable>
    );
}

      
const styles = StyleSheet.create({

    button_left: {
        // alignItems: 'center',
        right: 100,
        top: 280,
        paddingVertical: 20,
        paddingHorizontal: 36,
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
