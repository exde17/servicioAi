async function fetchVideos() {
    const formData = new FormData(document.getElementById('fetchForm'));
    const word = formData.get('word');

    await fetch(`${CONFIG.HOST}/get_video`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ word: word })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(err => { throw err; });
        }
    })
    .then(data => {
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = ''; // Limpia el contenido anterior
        const video = data;
        console.log(video);
            if (video.mime_type === 'video/mp4') {
                const videoPlayer = document.createElement('video');
                videoPlayer.width = 320;
                videoPlayer.height = 240;
                videoPlayer.controls = true;
                videoPlayer.src = `data:${video.mime_type};base64,${video.video_base64}`;
                responseDiv.appendChild(videoPlayer);
            } else if (video.mime_type === 'image/gif') {
                const gifImage = document.createElement('img');
                gifImage.width = 320;
                gifImage.height = 240;
                gifImage.src = `data:${video.mime_type};base64,${video.video_base64}`;
                responseDiv.appendChild(gifImage);
            }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'Error: ' + JSON.stringify(error);
    });
}

// fetchvideo.js
// import CONFIG from './config.js';

// async function fetchVideos() {
//     const formData = new FormData(document.getElementById('fetchForm'));
//     const word = formData.get('word');

//     await fetch(`${CONFIG.HOST}/get_video`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ word: word })
//     })
//     .then(response => {
//         if (response.ok) {
//             return response.json();
//         } else {
//             return response.json().then(err => { throw err; });
//         }
//     })
//     .then(data => {
//         const responseDiv = document.getElementById('response');
//         responseDiv.innerHTML = ''; // Limpia el contenido anterior
//         const video = data;
//         console.log(video);
//         if (video.mime_type === 'video/mp4') {
//             const videoPlayer = document.createElement('video');
//             videoPlayer.width = 320;
//             videoPlayer.height = 240;
//             videoPlayer.controls = true;
//             videoPlayer.src = `data:${video.mime_type};base64,${video.video_base64}`;
//             responseDiv.appendChild(videoPlayer);
//         } else if (video.mime_type === 'image/gif') {
//             const gifImage = document.createElement('img');
//             gifImage.width = 320;
//             gifImage.height = 240;
//             gifImage.src = `data:${video.mime_type};base64,${video.video_base64}`;
//             responseDiv.appendChild(gifImage);
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         document.getElementById('response').innerText = 'Error: ' + JSON.stringify(error);
//     });
// }