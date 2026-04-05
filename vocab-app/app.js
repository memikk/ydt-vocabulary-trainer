
// app.js - Enhanced with Levels, TTS, and Dashboard

const LEVELS_SIZE = 50;
let userState = {
    currentLevelIndex: -1, // -1 means no level selected
    completedWords: {}, // { "word": true }
    unknownWords: {},   // { "word": true }
    // We can also track progress per level manually or derive it
};

let currentSessionQueue = [];
let currentWord = null;
let isMeaningRevealed = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (typeof VOCAB_DATA === 'undefined' || !Array.isArray(VOCAB_DATA)) {
        document.body.innerHTML = '<h2 style="color:white; text-align:center; padding:20px;">Hata: Veri dosyası (data.js) yüklenemedi. Lütfen internet bağlantınızı kontrol edin veya dosyaları tekrar yükleyin.</h2>';
        return;
    }
    loadState();
    renderDashboard();
    setupEventListeners();
});

// --- Data Management ---

function loadState() {
    try {
        const saved = localStorage.getItem('ydt_vocab_state');
        if (saved) {
            userState = JSON.parse(saved);
        }
    } catch (e) {
        console.warn("LocalStorage error:", e);
    }
    // Ensure structure integrity
    if (!userState.completedWords) userState.completedWords = {};
    if (!userState.unknownWords) userState.unknownWords = {};
}

function saveState() {
    try {
        localStorage.setItem('ydt_vocab_state', JSON.stringify(userState));
    } catch (e) {
        console.warn("Save error:", e);
    }
    updateStatsUI();
}

function getLevels() {
    // Dynamically chunk VOCAB_DATA
    const levels = [];
    for (let i = 0; i < VOCAB_DATA.length; i += LEVELS_SIZE) {
        levels.push(VOCAB_DATA.slice(i, i + LEVELS_SIZE));
    }
    return levels;
}

// --- UI Rendering ---

function renderDashboard() {
    const levels = getLevels();
    const grid = document.getElementById('levels-grid');
    grid.innerHTML = '';

    levels.forEach((levelWords, index) => {
        const levelNum = index + 1;
        const total = levelWords.length;

        // Calculate progress
        const learnedCount = levelWords.filter(w => userState.completedWords[w.word]).length;
        const percent = Math.round((learnedCount / total) * 100);
        const isCompleted = learnedCount === total;

        const card = document.createElement('div');
        card.className = `level-card ${isCompleted ? 'completed' : ''}`;
        card.onclick = () => startLevel(index);

        card.innerHTML = `
            <span class="level-title">Bölüm ${levelNum}</span>
            <div class="level-progress-bg">
                <div class="level-progress-fill" style="width: ${percent}%"></div>
            </div>
            <div style="margin-top:5px; font-size:0.8rem; color:#888;">
                ${learnedCount} / ${total} Öğrenildi
            </div>
        `;
        grid.appendChild(card);
    });

    updateStatsUI();
}

function updateStatsUI() {
    // Total Learned
    const learnedCount = Object.keys(userState.completedWords).length;
    document.getElementById('total-learned').innerText = learnedCount;

    // Total Unknown
    const unknownCount = Object.keys(userState.unknownWords).length;
    document.getElementById('total-unknown').innerText = unknownCount;
    document.getElementById('unknown-count-btn').innerText = unknownCount;

    // Enable/Disable Master Review
    const btn = document.getElementById('master-review-btn');
    btn.disabled = unknownCount === 0;
    btn.onclick = () => startMasterReview();
}

// --- Study Logic ---

function startLevel(levelIndex) {
    userState.currentLevelIndex = levelIndex;
    const levels = getLevels();
    const allWords = levels[levelIndex];

    // Filter out words already learned to form the session queue
    // But if level is complete, maybe ask to reset? For now, just load all if complete or reset.
    // Use a simple approach: Load unlearned words first.
    let unlearned = allWords.filter(w => !userState.completedWords[w.word]);

    if (unlearned.length === 0) {
        // Reset/Re-study mode
        if (confirm("Bu bölümü zaten bitirdiniz. Tekrar çalışmak ister misiniz?")) {
            unlearned = [...allWords]; // Copy all
        } else {
            return;
        }
    }

    currentSessionQueue = shuffleArray(unlearned);
    switchToView('study');
    showNextWord();
}

function startMasterReview() {
    userState.currentLevelIndex = -2; // Special ID for Master Review
    // Gather all unknown word objects
    const unknownKeys = Object.keys(userState.unknownWords);

    // Find objects in VOCAB_DATA
    const words = VOCAB_DATA.filter(w => userState.unknownWords[w.word]);

    if (words.length === 0) return;

    currentSessionQueue = shuffleArray(words);
    switchToView('study');
    showNextWord();
}

function showNextWord() {
    if (currentSessionQueue.length === 0) {
        alert("Bölüm Tamamlandı!");
        switchToView('dashboard');
        renderDashboard();
        return;
    }

    currentWord = currentSessionQueue[0]; // Peek
    isMeaningRevealed = false;

    // UI Updates
    document.getElementById('word-display').innerText = currentWord.word;
    document.getElementById('type-display').innerText = currentWord.type || 'word';
    document.getElementById('meaning-container').classList.add('hidden');
    document.getElementById('btn-known').classList.add('hidden');
    document.getElementById('btn-unknown').classList.add('hidden');

    // Reset Animation
    const card = document.getElementById('flashcard');
    card.classList.remove('shake-animation');
}

function revealMeaning() {
    if (isMeaningRevealed) return;
    isMeaningRevealed = true;

    document.getElementById('meaning-display').innerText = currentWord.meaning;
    document.getElementById('meaning-container').classList.remove('hidden');

    // Show buttons
    document.getElementById('btn-known').classList.remove('hidden');
    document.getElementById('btn-unknown').classList.remove('hidden');
}

function handleResponse(isKnown) {
    if (!currentWord) return;

    if (isKnown) {
        // Mark as known
        userState.completedWords[currentWord.word] = true;
        // Remove from unknown if it was there
        if (userState.unknownWords[currentWord.word]) {
            delete userState.unknownWords[currentWord.word];
        }

        // Remove from queue
        currentSessionQueue.shift();

        saveState();
        showNextWord();
    } else {
        // Mark as unknown
        userState.unknownWords[currentWord.word] = true;
        saveState(); // Save immediately so it persists

        // Visual feedback
        const card = document.getElementById('flashcard');
        card.classList.add('shake-animation');
        setTimeout(() => card.classList.remove('shake-animation'), 500);

        // Move to end of queue to review again this session
        const w = currentSessionQueue.shift();
        currentSessionQueue.push(w);

        // Hide buttons to force user to look at word again? 
        // Or just go to next word? Let's go to next word for flow, 
        // but it will come back later in queue.
        showNextWord();
    }
}

// --- Audio ---
function speakCurrentWord() {
    if (!currentWord || !currentWord.word) return;

    // Basic browser TTS
    const utterance = new SpeechSynthesisUtterance(currentWord.word);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}

// --- Navigation ---

function switchToView(viewName) {
    const dashboard = document.getElementById('dashboard-view');
    const study = document.getElementById('study-view');
    const homeBtn = document.getElementById('home-btn');

    if (viewName === 'study') {
        dashboard.classList.add('hidden');
        study.classList.remove('hidden');
        homeBtn.classList.remove('hidden');
    } else {
        dashboard.classList.remove('hidden');
        study.classList.add('hidden');
        homeBtn.classList.add('hidden');
        renderDashboard(); // Refresh stats
    }
}

function setupEventListeners() {
    // Home Button
    document.getElementById('home-btn').onclick = () => switchToView('dashboard');

    // Flashcard Tap
    document.getElementById('flashcard').onclick = (e) => {
        // Don't trigger if audio button clicked
        if (e.target.closest('#audio-btn')) return;
        revealMeaning();
    };

    // Audio Button
    document.getElementById('audio-btn').onclick = (e) => {
        e.stopPropagation(); // Prevent reveal
        speakCurrentWord();
    };

    // Response Buttons
    document.getElementById('btn-known').onclick = (e) => {
        e.stopPropagation();
        handleResponse(true);
    };

    document.getElementById('btn-unknown').onclick = (e) => {
        e.stopPropagation();
        handleResponse(false);
    };
}

// Helper
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
