// Global assignments
const backend_call = 'http://localhost:7000/reencode'
// Getting environmnet variables 
    // window = window = await import('./env-config.js');
    // backend_url = window.env.BACKEND_URL;
    // backend_port = window.env.BACKEND_PORT;
    // console.error('error: nanana');

// Reencode buttom
const button = document.getElementById('reencode_button');
button.addEventListener('click', async (event) => {
    event.preventDefault();
    try {
        const response = await reencode_call();
        display_response(response)
    } catch (err) {
        console.error(`error: ${err}`);
    }
});

async function reencode_call(){
    const video_url = document.getElementById('video_url').value;
    const response = await fetch(backend_call, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_source:video_url
        })
    });
    console.log(`post to ${video_url} with method ${response.method} and body ${response.body}`);
    if (response.ok){
        return response
    }else{
        throw new Error(`Error: ${response.text()}`);
    }
}

function display_response(response){
    // Getting return message displayed to the user
    let response_message = document.getElementById('response_message');
    if (response.ok){
        response_message.textContent = 'Sua requisição foi recebida e seu vídeo será reencodado!';
        response_message.style.color = 'green';
    }
    // switch (await response.status()) {
    //     case 200:
            
    //         break;
    
    //     default:
    //         break;
    // }
}