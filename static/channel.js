document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    var input = document.querySelector('#message');

    function initializeConversation(previousMessages){
        previousMessages.forEach(formatMessage);
    }
    
    input.addEventListener("keyup", function(event) {
        if (event.keyCode == 13) {
            document.querySelector('#submit-button').click();
        }
    });

    socket.on('connect', () => {

        document.querySelector('#submit-button').onclick = () => {
            var message = document.querySelector('#message').value;
            const color = document.querySelector('#message').getAttribute('color');
            document.querySelector('#message').value = "";
            socket.emit('submit message',{'message': message, 'color': color});
      };

    });

    socket.on('announce', data => {
        displayMessage(data);
    });


    function displayMessage(data){
        const message = document.createElement('li');
        message.style.color = data.color;

        const timestamp = document.createElement('span');
        timestamp.id = 'timestamp';
        message.appendChild(timestamp);

        const nickname = document.createElement('span');
        nickname.id = 'nickname';
        message.appendChild(nickname);

        const content = document.createElement('span');
        content.id = 'content';
        message.appendChild(content);

        timestamp.textContent = '[' + data.timestamp + '] ';
        nickname.textContent = data.nickname;
        content.textContent = ": " + data.message;

        document.querySelector('#conversation').append(message);

        updateScroll();
    }

    function updateScroll(){
        var element = document.getElementById("mesgs");
        element.scrollTop = element.scrollHeight;
    }

});



