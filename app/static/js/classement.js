let currentUsername;
        
document.addEventListener("DOMContentLoaded", () => {
    currentUsername = document.getElementById("current-username").value;
});

function onGameSelect(event) {
    const gameId = event.target.value;
    if (gameId) {
        fetchScores(gameId);
    } else {
        updateScoresTable([]); // Efface le contenu du tableau
    }
}

async function fetchScores(gameId) {
    const response = await fetch(`/api/scores?game_id=${gameId}`);
    const data = await response.json();
    console.log('Data received:', data); // Ajout d'un message de débogage

    if (data.scores) {
        updateScoresTable(data.scores);
    } else {
        console.error('No scores received'); // Ajout d'un message d'erreur
    }
}

function updateScoresTable(scores) {
    console.log('Updating scores table with:', scores);
    const tbody = document.querySelector('#scoresTable tbody');
    tbody.innerHTML = '';

    let position = 1;
    for (const score of scores) {
        const isCurrentUser = score.username === currentUsername;
        const highlightedClass = isCurrentUser ? "bg-red-900" : "";
        const tr = document.createElement('tr');
        tr.className = highlightedClass;

        const positionTd = document.createElement('td');
        positionTd.textContent = position;
        tr.appendChild(positionTd);

        const usernameTd = document.createElement('td');
        usernameTd.textContent = score.username;
        tr.appendChild(usernameTd);

        const scoreTd = document.createElement('td');
        scoreTd.textContent = score.score;
        tr.appendChild(scoreTd);

        tbody.appendChild(tr);
        position++;
    }
}