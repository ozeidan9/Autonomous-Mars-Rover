import io from 'socket.io-client';

const Socket = io.connect('http://localhost:10000', {});

export default Socket;