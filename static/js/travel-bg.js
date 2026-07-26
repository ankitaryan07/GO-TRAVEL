/* Floating travel symbols background — har page pe add hota hai */
(function () {
    const symbols = ['✈️','🏖️','🗺️','🧳','🏔️','🚂','⛵','🏝️','📷','🎒','🌍','🚁','🏕️','🛫','🧭'];
    const bg = document.createElement('div');
    bg.className = 'travel-bg';
    const count = 14;
    for (let i = 0; i < count; i++) {
        const s = document.createElement('span');
        s.textContent = symbols[i % symbols.length];
        s.style.left = Math.random() * 100 + '%';
        s.style.top = Math.random() * 100 + '%';
        s.style.fontSize = (20 + Math.random() * 30) + 'px';
        s.style.animationDuration = (15 + Math.random() * 20) + 's';
        s.style.animationDelay = (Math.random() * 5) + 's';
        bg.appendChild(s);
    }
    document.body.appendChild(bg);
})();
