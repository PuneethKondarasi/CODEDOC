document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const output = document.getElementById("output");
    const page3 = document.querySelector(".page_3");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        output.style.display = "block";
        page3.style.display = "grid";
    });
});

function searchStudyMaterial(topic) {
    const cx = 'Your Google Custom Search Engine ID';
    const apiKey = 'Your Google API Key'; 

    const url = `https://www.googleapis.com/customsearch/v1?q=${topic}&cx=${cx}&key=${apiKey}&num=5`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Google Search Results:', data);
            displaySearchResults(data.items);
        })
        .catch(error => console.error('Error fetching Google search results:', error));
}

function displaySearchResults(results) {
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "<h3>Here are some study materials for you: </h3>";

    results.forEach(item => {
        const link = document.createElement("a");
        link.href = item.link;
        link.textContent = item.title;
        outputDiv.appendChild(link);
        outputDiv.appendChild(document.createElement("br"));
    });
}

function searchYouTubePlaylists(topic) {
    const apiKey = 'Your YouTube API Key';
    const maxResults = 4;

    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${topic}&key=${apiKey}&maxResults=${maxResults}&type=playlist`;

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('YouTube Playlists:', data);
            return data.items;
        })
        .catch(error => console.error('Error fetching YouTube playlists:', error));
}

async function displayYouTubePlaylists(playlists) {
    const page3 = document.querySelector(".page_3");
    page3.innerHTML = "";

    for (const playlist of playlists) {
        const playlistDiv = document.createElement("div");
        playlistDiv.classList.add("playlist");

        const playlistTitle = document.createElement("h3");
        playlistTitle.textContent = playlist.snippet.title;

        const iframe = document.createElement("iframe");
        iframe.src = `https://www.youtube.com/embed/videoseries?list=${playlist.id.playlistId}`;
        iframe.width = "460";
        iframe.height = "250";
        iframe.allowFullscreen = true;
        iframe.title = playlist.snippet.title;

        playlistDiv.appendChild(playlistTitle);
        playlistDiv.appendChild(iframe);

        page3.appendChild(playlistDiv);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        const topic = document.getElementById("search").value;

        const playlists = await searchYouTubePlaylists(topic);
        displayYouTubePlaylists(playlists);

        searchStudyMaterial(topic);
    });
});

