// Listen to socket.io messages on app port 4040.
var server  = require('http').createServer().listen(4040);
var io      = require('socket.io').listen(server);

// Do something with all sockets on succesfull connection.
io.sockets.on('connection', function (socket) {
    // Listen for 'subscribe' event on each socket.
    socket.on('subscribe', function (channel) {
        // When event sends message, join socket to given channel.
        socket.join(channel);
    });
});

// Create redis client instance.
var redis  = require('redis');
var client = redis.createClient();

// Subscribe redis client to two channels.
client.on('ready', function() {
    client.subscribe('go');
    client.subscribe('chat');
});

// Upon receiving an event from redis channel, post the event to socket.io.
client.on('message', function (channel, message) {
    // Get all sockets in channel with same name as redis client channel.
    io.sockets.in(channel)
    // Emit 'message' event to socket.io in browser.
              .emit('message', { channel: channel, message: message });
});
