document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelector('#submit-button').onclick = () => {

            const message = document.querySelector('#message').value;
            socket.emit('submit message',{'message': message});
            };

    });

    socket.on('announce message', data => {
        const li = document.createElement('li');
        li.innerHTML = data.message;
        document.querySelector('#conversation').append(li);

    });

});

