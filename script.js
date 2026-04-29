// Zmienna globalna do przechowywania stanu 
let isPaused = false;

// Funkcja nasłuchująca wciśnięcia Spacji
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
        event.preventDefault(); // Zapobiega przewijaniu strony spacją
        isPaused = !isPaused;   // Zmienia stan na przeciwny (włącz/wyłącz)
        
        // Jeśli właśnie odpausowaliśmy, musimy ręcznie wznowić pętlę
        if (!isPaused) {
            draw();
        }
    }
});

function draw() {
    // Jeśli jest pauza, przerywamy funkcję (nie rysujemy nowej klatki, ale stara zostaje)
    // UWAGA: Logikę sprawdzania pauzy przy requestAnimationFrame zostawiamy na końcu

    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Tarcza (Tło)
    ctx.beginPath();
    ctx.arc(195, 150, 140, 0, 2 * Math.PI);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.stroke();

    // --- NOWOŚĆ: RYSOWANIE LICZB (1-12) ---
    ctx.font = "bold 24px Arial"; // Ustawienie czcionki
    ctx.fillStyle = "white";      // Kolor liczb (biały dobrze widać na szarym)
    ctx.textAlign = "center";     // Wyrównanie do środka punktu X
    ctx.textBaseline = "middle";  // Wyrównanie do środka punktu Y

    for (let num = 1; num <= 12; num++) {
        // 1. Obliczamy kąt dla każdej liczby
        // Każda godzina to PI/6 (30 stopni). Odejmujemy PI/2, by zacząć od góry (12:00)
        const angle = num * (Math.PI / 6) - (Math.PI / 2);

        // 2. Obliczamy pozycję X i Y (trygonometria)
        // 195, 150 to środek tarczy
        // 115 to promień rozmieszczenia cyfr (nieco mniejszy niż tarcza 140)
        const x = 195 + Math.cos(angle) * 115;
        const y = 150 + Math.sin(angle) * 115;

        // 3. Rysujemy liczbę
        ctx.fillText(num.toString(), x, y);
    }

    // --- OBLICZENIA CZASU ---
    const now = new Date();

    const textCzasu = now.toLocaleTimeString(); 
    const elementCzasu = document.getElementById("Czas");
    if (elementCzasu) {
        elementCzasu.innerText = textCzasu;
    }

    // Sekundy
    const seconds = now.getSeconds() + now.getMilliseconds() / 1000;
    const angleSeconds = seconds * (Math.PI / 30) - (Math.PI / 2);

    // Minuty
    const mins = now.getMinutes() + now.getSeconds() / 60;
    const angleMins = mins * (Math.PI / 30) - (Math.PI / 2);

    // Godziny
    const hours = (now.getHours() % 12) + now.getMinutes() / 60;
    const angleHours = hours * (Math.PI / 6) - (Math.PI / 2);

    //RYSOWANIE WSKAZÓWEK

    // 1. Godzinowa
    ctx.save();
    ctx.translate(195, 150);
    ctx.rotate(angleHours);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(80, 0);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 8;
    ctx.lineCap = "round";
    ctx.stroke();
    ctx.restore();

    // 2. Minutowa
    ctx.save();
    ctx.translate(195, 150);
    ctx.rotate(angleMins);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(115, 0);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 6;
    ctx.lineCap = "round";
    ctx.stroke();
    ctx.restore();

    // 3. Sekundowa
    ctx.save();
    ctx.translate(195, 150);
    ctx.rotate(angleSeconds);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(125, 0);
    ctx.strokeStyle = "red";
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.stroke();
    ctx.restore();

    // Środek
    ctx.beginPath();
    ctx.arc(195, 150, 10, 0, 2 * Math.PI);
    ctx.fillStyle = "black";
    ctx.fill();

    // --- PAUZA: Sprawdzenie czy rysować dalej ---
    if (!isPaused) {
        requestAnimationFrame(draw);
    }
}

// Pierwsze wywołanie
draw();