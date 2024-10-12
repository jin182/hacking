async function exploit() {
    // Start new game
    const startResponse = await fetch("/api/start-game", {
        method: "POST"
    });
    const gameData = await startResponse.json();
    const gameId = gameData.gameId;
    
    // Map all cards
    const cardMap = {};
    for (let i = 0; i < 12; i++) {
        const revealResponse = await fetch("/api/reveal-card", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gameId, cardIndex: i })
        });
        const cardData = await revealResponse.json();
        if (!cardMap[cardData.cardImage]) {
            cardMap[cardData.cardImage] = [];
        }
        cardMap[cardData.cardImage].push(i);
    }
    
    // Submit only matching pairs
    for (let card in cardMap) {
        const [first, second] = cardMap[card];
        await fetch("/api/check-match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                gameId,
                firstCardIndex: first,
                secondCardIndex: second
            })
        });
    }
    
    // Get flag
    const finalResponse = await fetch("/api/game-over", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gameId })
    });
    const result = await finalResponse.json();
    console.log("Flag:", result.finalScore);
}

// Run exploit
exploit();
