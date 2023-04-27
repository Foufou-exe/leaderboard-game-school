
async function addGame(event) {
    event.preventDefault();

    const gameNameInput = document.getElementById('game-name-input');
    const gameName = gameNameInput.value;

    if (!gameName) {
        alert('Veuillez entrer un nom de jeu.');
        return;
    }

    try {
        const response = await fetch('/api/add_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: gameName })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Le jeu a été ajouté avec succès.');
            location.reload(); // Recharge la page pour afficher le nouveau jeu dans la liste.
        } else {
            alert(`Erreur : ${data.error}`);
        }
    } catch (error) {
        console.error('Une erreur est survenue :', error);
        alert('Une erreur est survenue lors de l\'ajout du jeu.');
    }
}

function onAddScore(event) {
    event.preventDefault();
    const gameSelect = document.getElementById('game-select');
    const gameId = gameSelect.value;
    const scoreInput = document.getElementById('score-input');
    const score = scoreInput.value;
    const dateInput = document.getElementById('date-input');
    const date = dateInput.value;
    fetch('/api/add_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ game_id: gameId, score: score, date: date }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            location.reload();
        }
    });
}
