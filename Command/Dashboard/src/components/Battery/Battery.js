
// import './Battery.css';


const input =  prompt("Enter battery level: ");



export const Battery = (input) => {
    
    return (
        <html>
            <body>
                <meter id="fuel">
                    val={input}
                </meter>
            </body>   
        </html>
    )
}