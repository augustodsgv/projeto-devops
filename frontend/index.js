import env  from './env.js';
const BACKEND_URL = "http://" + env.BACKEND_URL;
const BACKEND_PORT = env.BACKEND_PORT;


async function loadTableData() {
    const tableBody = document.getElementById('videoTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    const video_list = await fetch_video_list();
    let videos
    if (video_list.ok){
        videos = await video_list.json()
        console.log(videos)
    }
    videos.forEach(async video => {
        const row = document.createElement('tr');

        // File name column
        const nameCell = document.createElement('td');
        nameCell.textContent = video;
        row.appendChild(nameCell);

        // Edit button
        const editCell = document.createElement('td');
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.onclick = () => {
            window.location.href = `/edit.html?name=${video}`;
        };
        editCell.appendChild(editButton);
        row.appendChild(editCell);

        // Delete button
        const deleteCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = async () => {
            const delete_response = await delete_video(video);
            if (delete_response.ok){
                // TODO: exibir mensagem de êxito
            }
        };
        deleteCell.appendChild(deleteButton);
        row.appendChild(deleteCell);

        // Download button
        const downloadCell = document.createElement('td');
        const downloadButton = document.createElement('button');
        downloadButton.textContent = 'Download';
        downloadButton.addEventListener('click', async () => {
            let download_response;
            try {
                download_response = await download_video(video);
                if (download_response.ok){
                    const blob = await download_response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = video;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                }else{
                    throw new Error(`Error: ${download_response.text()}`);
                }
            } catch (err) {
                console.error(`error: ${err}`);
            }
        })
        downloadCell.appendChild(downloadButton);
        row.appendChild(downloadCell);
        tableBody.appendChild(row);
    });
}

async function fetch_video_list(){
    const response = await fetch(BACKEND_URL+':'+BACKEND_PORT+"/list", {
        method: 'GET',
    });
    return response
}

// Load table data on page load
window.onload = loadTableData;

// const selectFileButton = document.getElementById('select-file-button');
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', () => {
    const selectedFile = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', selectedFile);
    fetch(BACKEND_URL+':'+BACKEND_PORT+'/upload',{
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

async function download_video(video_name){
    const response = await fetch(BACKEND_URL+':'+BACKEND_PORT+'/download', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_name:video_name
        })
    });
    return response;
}

async function delete_video(video_name){
    const response = await fetch(
        BACKEND_URL+':'+BACKEND_PORT+'/delete_video?video_name='+video_name, {
        method: 'delete',
    });
    return response;
}