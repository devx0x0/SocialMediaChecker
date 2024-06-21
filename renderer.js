document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('checkUsernameButton').addEventListener('click', checkUsername);
    document.getElementById('manualSearchButton').addEventListener('click', performManualSearch);
    document.getElementById('saveResultsButton').addEventListener('click', saveResults);
    document.getElementById('clearResultsButton').addEventListener('click', clearResults);
});

let resultsData = [];

const checkUsername = () => {
    const username = document.getElementById('usernameInput').value;
    const statusMessage = document.getElementById('statusMessage');
    const results = document.getElementById('results');

    statusMessage.textContent = 'Checking...';
    results.innerHTML = '';

    window.ipcRenderer.invoke('check-username', { username }).then(response => {
        console.log('Response:', response);
        statusMessage.textContent = '';
        resultsData = response;
        results.innerHTML = response.map(result => `
            <p style="color: neon-green; font-weight: bold;">
                ${result.platform}: ${result.exists ? 'Available' : 'Taken'} - <a href="${result.url}" target="_blank">${result.url}</a>
            </p>
        `).join('');
    }).catch(error => {
        statusMessage.textContent = 'Error checking username';
        console.error(error);
    });
};

const performManualSearch = () => {
    const website = document.getElementById('websiteInput').value;
    const username = document.getElementById('manualUsernameInput').value;
    const manualResults = document.getElementById('manualResults');

    manualResults.innerHTML = 'Searching...';

    window.ipcRenderer.invoke('manual-search', { website, username }).then(response => {
        console.log('Manual Search Response:', response);
        const result = JSON.parse(response[0])[0]; // Correctly parse the response
        manualResults.innerHTML = `
            <p style="color: neon-green; font-weight: bold;">
                ${result.platform}: ${result.exists ? 'Available' : 'Taken'} - <a href="${result.url}" target="_blank">${result.url}</a>
            </p>
        `;
    }).catch(error => {
        manualResults.innerHTML = 'Error performing manual search';
        console.error(error);
    });
};

const saveResults = () => {
    const text = resultsData.map(result => `${result.platform}: ${result.exists ? 'Available' : 'Taken'} - ${result.url}`).join('\n');
    window.ipcRenderer.invoke('save-results', { text });
};

const clearResults = () => {
    window.ipcRenderer.invoke('clear-results');
};

window.ipcRenderer.on('clear-results', () => {
    document.getElementById('results').innerHTML = '';
    document.getElementById('manualResults').innerHTML = '';
});