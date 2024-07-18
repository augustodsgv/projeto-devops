
async function set_title(){
    let title_name = document.getElementById('titulo-pagina');
    const nome_arquivo = await get_nome_arquivo();
    title_name.textContent = 'Editando arquivo \"' + nome_arquivo + "\"";
}

async function get_nome_arquivo(){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('name');
}

window.onload = set_title;

// Enviar o vídeo para processar
const process_button = document.getElementById('botao-processar-video');
process_button.addEventListener('click', async (event) => {
    const video_name = await get_nome_arquivo();
    const response = await processar_video(video_name);
    if (response.ok){
        window.location.href = `/`;
    }
});

async function processar_video(video_name){
    let response
    // Checando se é para cortar
    const is_cut = document.getElementById('is_cut').checked;
    if (is_cut){
        const video_begin = Number(document.getElementById('video_begin').value);
        const video_end = Number(document.getElementById('video_end').value);
        console.log(JSON.stringify({
            video_name:video_name,
            video_begin:video_begin,
            video_end:video_end}))
        response = await fetch("http://localhost:7000/cut", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_name:video_name,
                video_begin:video_begin,
                video_end:video_end
            })
        });
        if (!response.ok){      // Erro ao cortar o vídeo
            return response;
        }
    }

    return response;
}