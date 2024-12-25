async function fetchRandomCard() {
    try {
        // First, fetch all cards
        const response = await fetch('https://db.ygoprodeck.com/api/v7/cardinfo.php');
        const data = await response.json();
        
        // Get a random card from the data
        const randomIndex = Math.floor(Math.random() * data.data.length);
        const randomCard = data.data[randomIndex];
        
        displayCard(randomCard);
    } catch (error) {
        console.error('Error fetching card:', error);
        // Show error message to user
        const container = document.getElementById('card-container');
        container.innerHTML = `
            <div class="error-message">
                <p>Sorry, couldn't load the card. Please try again later.</p>
            </div>
        `;
    }
}

function displayCard(card) {
    const container = document.getElementById('card-container');
    const levelOrRank = card.level || card.rank || 0;
    const stars = '★'.repeat(levelOrRank);
    
    container.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h2>${card.name}</h2>
                <div class="level-stars">
                    ${stars}
                </div>
            </div>
            
            <div class="attribute-text">
                ${card.attribute || ''}
            </div>

            <div class="card-image-container">
                <img src="${card.card_images[0].image_url_cropped}" alt="${card.name}" class="card-image">
            </div>

            <div class="card-type">
                [${card.race}/${card.type}]
            </div>

            <div class="card-description">
                ${card.desc}
            </div>

            <div class="card-stats-bottom">
                ${card.atk !== undefined ? `ATK/${card.atk}` : ''}
                ${card.def !== undefined ? `DEF/${card.def}` : ''}
            </div>
        </div>
    `;
}

// Add loading state to button
const generateBtn = document.getElementById('generate-btn');
generateBtn.addEventListener('click', async () => {
    generateBtn.disabled = true;
    generateBtn.textContent = 'Loading...';
    await fetchRandomCard();
    generateBtn.disabled = false;
    generateBtn.textContent = 'Generate Random Card';
});

// Load initial card when page loads
fetchRandomCard();
