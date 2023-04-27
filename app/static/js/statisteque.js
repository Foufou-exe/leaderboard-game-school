document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/game_stats')
        .then(response => response.json())
        .then(data => {
            const gameData = data.gameStats;
            renderPieChart(gameData);
            renderTable(gameData);
        });
});
function renderPieChart(gameData) {
    const pieTrace = {
        type: 'pie',
        labels: gameData.map(game => game.name),
        values: gameData.map(game => game.wins + game.losses),
        textinfo: 'label+percent',
        textposition: 'inside',
        automargin: true
    };

    const pieLayout = {
        title: 'Parties jouées par jeu',
        height: 400,
        width: 400,
        plot_bgcolor: 'rgba(0, 0, 0, 0)', // Transparent
        paper_bgcolor: 'rgba(0, 0, 0, 0)', // Transparent
        margin: {
            t: 30,
            b: 10,
            l: 10,
            r: 10
        },
        showlegend: false
    };

    Plotly.newPlot('pie-chart', [pieTrace], pieLayout);
}

function renderTable(gameData) {
    const tableBody = document.getElementById('game-stats').getElementsByTagName('tbody')[0];

    gameData.forEach(game => {
        const row = tableBody.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        cell1.textContent = game.name;
        cell2.textContent = game.wins + game.losses;
        row.classList.add('bg-gray-800', 'p-2');
    });
}