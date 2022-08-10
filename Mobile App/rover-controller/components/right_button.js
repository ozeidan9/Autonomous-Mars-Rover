import React from 'react';
import { Text, View, StyleSheet, Pressable } from 'react-native';


function sendAPI_right(){
    // const controls = JSON.stringify({ direction: val });
    // axios.post('http://localhost:4000/mov_ctrl', controls);
    try {
        fetch('http://192.168.43.50:11000/mov_ctrl', {
        method : 'post',
        mode : 'no-cors',
        headers : {
            'Accept' : 'application/json',
            'Content-type' : 'application/json'
        },
        body : JSON.stringify({
            direction: '1540', //0000100000000100
                        
        })
        });
    }catch(e){
        console.log(e);
    }
}

export default function RIGHTButton(props) {
    const { title = 'Right' } = props;
    return (
        <Pressable style={styles.button_right} onPress={()=>{sendAPI_right()}}>
        <Text style={styles.text}>{title}</Text>
        </Pressable>
    );
}
      
const styles = StyleSheet.create({
   
    button_right: {
        // alignItems: 'center',
        right: -100,
        top: 220,
        paddingVertical: 20,
        paddingHorizontal: 32,
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
