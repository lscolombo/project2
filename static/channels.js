document.addEventListener('DOMContentLoaded', () => {


});

function saveChannel(channel){
    localStorage.setItem('channel', channel.id);
}

function saveNickname(nickname){
    localStorage.setItem('nickname', nickname);
}

function clearChannel(){
    localStorage.removeItem('channel');
}

function getChannel(){
    return(localStorage.getItem('channel'));
}