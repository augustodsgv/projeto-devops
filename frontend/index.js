import env  from './env.js';
const BACKEND_URL = "http://" + env.BACKEND_URL;
const BACKEND_PORT = env.BACKEND_PORT;


async function loadTableData() {
    const tableBody = document.getElementById('videoTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    const response = await fetch_video_list();
    let videos
    if (response.ok){
        videos = await response.json()
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
            // Redirect to edit page (implement your logic here)
            window.location.href = `/edit.html?name=${video}`;
        };
        editCell.appendChild(editButton);
        row.appendChild(editCell);

        // Delete button
        const deleteCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => {
            // Call API to delete video (implement your logic here)
            fetch(`/api/delete/${video.id}`, { method: 'DELETE' })
                .then(response => {
                    if (response.ok) {
                        // Remove video from the array and reload table data
                        const index = videos.findIndex(v => v.name === video);
                        if (index !== -1) {
                            videos.splice(index, 1);
                            loadTableData();
                        }
                    } else {
                        alert('Failed to delete video');
                    }
                });
        };
        deleteCell.appendChild(deleteButton);
        row.appendChild(deleteCell);

        // Download button
        const downloadCell = document.createElement('td');
        const downloadButton = document.createElement('button');
        downloadButton.textContent = 'Download';
        downloadButton.addEventListener('click', async () => {
            let response;
            try {
                response = await download_video(video);
                if (response.ok){
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = video;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                
                }else{
                    throw new Error(`Error: ${response.text()}`);
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

// // Botão de download
// const download_button = document.getElementById('download_button');
// download_button.addEventListener('click', async (event) => {
//     event.preventDefault();
//     let response;
//     try {
//         response = await download_video();
//         if (response.ok){
//             const blob = await response.blob();
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.style.display = 'none';
//             a.href = url;
//             a.download = `${document.getElementById('video_to_download').value}`;
//             document.body.appendChild(a);
//             a.click();
//             window.URL.revokeObjectURL(url);
        
//         }else{
//             throw new Error(`Error: ${response.text()}`);
//         }
//     } catch (err) {
//         console.error(`error: ${err}`);
//     }
//     // console.log("passou aqui");
//     // display_download_response(response);
// });
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
    return response
}