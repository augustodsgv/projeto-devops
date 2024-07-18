// Global assignments
// const reencode_url = 'http://localhost:7000/reencode'
// // Getting environmnet variables 
//     // window = window = await import('./env-config.js');
//     // backend_url = window.env.BACKEND_URL;
//     // backend_port = window.env.BACKEND_PORT;
//     // console.error('error: nanana');

// // Reencode buttom
// const reencode_button = document.getElementById('reencode_button');
// reencode_button.addEventListener('click', async (event) => {
//     event.preventDefault();
//     try {
//         const response = await reencode_call();
//         display_reencode_response(response)
//     } catch (err) {
//         console.error(`error: ${err}`);
//     }
// });

// async function reencode_call(){
//     const video_url = document.getElementById('video_url').value;
//     const response = await fetch(reencode_url, {
//         method: 'post',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             video_source:video_url
//         })
//     });
//     console.log(`post to ${video_url} with method ${response.method} and body ${response.body}`);
//     if (response.ok){
//         return response
//     }else{
//         throw new Error(`Error: ${response.text()}`);
//     }
// }

// function display_reencode_response(response){
//     // Getting return message displayed to the user
//     let response_message = document.getElementById('reencode_msg');
//     if (response.ok){
//         response_message.textContent = 'Sua requisição foi recebida e seu vídeo será reencodado!';
//         response_message.style.color = 'green';
//     }
//     // switch (await response.status()) {
//     //     case 200:
            
//     //         break;
    
//     //     default:
//     //         break;
//     // }
// }


// Download button
const download_url = 'http://localhost:7000/download'
const download_button = document.getElementById('download_button');
download_button.addEventListener('click', async (event) => {
    event.preventDefault();
    let response;
    try {
        response = await download_video();
        if (response.ok){
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${document.getElementById('video_to_download').value}.mp4`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        
        }else{
            throw new Error(`Error: ${response.text()}`);
        }
    } catch (err) {
        console.error(`error: ${err}`);
    }
    console.log("passou aqui");
    display_download_response(response);
});
async function download_video(){
    const video_name = document.getElementById('video_to_download').value;
    const response = await fetch(download_url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_name:video_name
        })
    });
    return response
}

function display_download_response(response){
    console.log(response.text())
    // Getting return message displayed to the user
    let response_message = document.getElementById('download_msg');
    if (response.ok){
        response_message.textContent = 'Iniciando download do arquivo!';
        response_message.style.color = 'green';
    }else{
        response_message.textContent = 'Erro ao fazer o download!';
        response_message.style.color = 'red';
    }
}

// const selectFileButton = document.getElementById('select-file-button');
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', () => {
    console.log("entrou aqui!");
    const selectedFile = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', selectedFile);
    fetch('http://localhost:7000/upload',{
        method: 'POST',
        body: formData
    })
    .then(response =>{
        display_upload_response(response);
        console.log('Selected file:', selectedFile.name);
    });
})

async function display_upload_response(response){
    // Getting return message displayed to the user
    let response_message = document.getElementById('upload_msg');
    if (await response.ok){
        response_message.textContent = 'Upload do arquivo com sucesso!';
        response_message.style.color = 'green';
    }else{
        response_message.textContent = 'Erro ao fazer o upload do arquivo!';
        response_message.style.color = 'red';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://localhost:7000/list')
        .then(response => response.json(), {method: 'POST'})
        .then(data => {
            const tableBody = document.querySelector('#file-table tbody');
            data.forEach(file => {
                const row = document.createElement('tr');

                const idCell = document.createElement('td');
                idCell.textContent = file.id;
                row.appendChild(idCell);

                const nameCell = document.createElement('td');
                nameCell.textContent = file.name;
                row.appendChild(nameCell);

                const urlCell = document.createElement('td');
                const urlLink = document.createElement('a');
                urlLink.href = file.url;
                urlLink.textContent = file.url;
                urlCell.appendChild(urlLink);
                row.appendChild(urlCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching files:', error);
        });
});