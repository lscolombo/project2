document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    var input = document.querySelector('#message');
    
    input.addEventListener("keyup", function(event) {
        if (event.keyCode == 13) {
            document.querySelector('#submit-button').click();
        }
    });

    socket.on('connect', () => {

        document.querySelector('#submit-button').onclick = () => {
            var message = document.querySelector('#message').value;
            document.querySelector('#message').value = "";
            socket.emit('submit message',{'message': message});
      };

    });

    socket.on('announce', data => {
        console.log('holache:','holache');
        const li = document.createElement('li');
        li.innerHTML = data.message;
        document.querySelector('#conversation').append(li);
    });

});

