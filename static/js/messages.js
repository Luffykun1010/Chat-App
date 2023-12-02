let input_message = $('#input-message')
let msg_body =$('#chat-msg')
let sendForm = $('#sendForm')
const chatSocket = new WebSocket(
    'ws://' + window.location.host
);
chatSocket.onopen = async function (e) {
    console.log('open', e)
    sendForm.on('submit', function(e) {
        e.preventDefault()
        let message = input_message.val()
        let data = {
            'message' : message,
        }
        data = JSON.stringify(data)
        chatSocket.send(data)
        input_message.val('');
        return false;
    })
}
chatSocket.onmessage = async function (e) {
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    if (message) {
        let msg_element = '<div class="row">'
            msg_element += '<div class="col-4 col-md-6"></div>'
            msg_element += '<div class="col-8 col-md-6"><div class="card" style="margin: 2.5vh 0 0 2vh;border: 0.5vh #055f6d solid;border-radius:3vh;width: fit-content;float: right;">'
            msg_element += '<div class="card-body" style="padding: 1rem 1rem;">' + message + '</div>'
            msg_element += '</div></div></div>'
        document.querySelector('#chat-msg').innerHTML += msg_element;
    } else {
        alert('The message is empty');
    }
}
chatSocket.onclose = async function (e) {
    console.log('close', e)
}