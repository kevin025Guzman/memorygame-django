const tablero = document.getElementById('tablero');
const intentosSpan = document.getElementById('intentos');
const tiempoSpan = document.getElementById('tiempo');

// Audios y modales
const audioMain = document.getElementById('audioMain');
const audioWin = document.getElementById('audioWin');
const audioLose = document.getElementById('audioLose');
const audioMatch = document.getElementById('audioMatch');
const modalWin = new bootstrap.Modal(document.getElementById('modalWin'));
const modalLose = new bootstrap.Modal(document.getElementById('modalLose'));

audioMatch.volume = 0.5;
audioMain.volume = 0.4;
audioWin.volume = 0.6;
audioLose.volume = 0.6;

let intentos = parseInt(intentosSpan.textContent);
let tiempo = parseInt(tiempoSpan.textContent);
let cartasVolteadas = [];
let bloqueado = false;
let cuentaRegresiva = null;
let juegoIniciado = false;

// Crear pares de cartas
const simbolos = [
    'cerdo.png', 'cocodrilo.png', 'gorila.png', 'leon.png',
    'panda.png', 'pinguino.png', 'pollo.png', 'tigre.png'
];
let cartas = [...simbolos, ...simbolos];
cartas.sort(() => Math.random() - 0.5);


// Crear tablero
cartas.forEach(simbolo => {
    const div = document.createElement('div');
    div.classList.add('memory-card');
    div.dataset.simbolo = simbolo;

    const img = document.createElement('img');
    img.src = `/static/memory_game/img/cartas/${simbolo}`;
    img.alt = simbolo.split('.')[0];
    img.classList.add('carta-img');
    img.style.visibility = 'hidden';

    div.appendChild(img);
    div.addEventListener('click', () => voltearCarta(div));
    tablero.appendChild(div);
});


function iniciarJuego() {
    // Música y timer juntos
    if (audioMain.paused) audioMain.play();
    cuentaRegresiva = setInterval(() => {
        tiempo--;
        tiempoSpan.textContent = tiempo;
        if (tiempo <= 0) {
            clearInterval(cuentaRegresiva);
            audioMain.pause();
            audioMain.currentTime = 0;
            registrarResultado("derrota", 0);
            audioLose.play();
            modalLose.show();
        }
    }, 1000);
}


function voltearCarta(carta) {
    // Arranca juego en el primer click
    if (!juegoIniciado) {
        iniciarJuego();
        juegoIniciado = true;
    }

    // si está bloqueado, ya está emparejada o ya está volteada → no hacer nada
    if (bloqueado || carta.classList.contains('matched') || cartasVolteadas.includes(carta)) return;

    const img = carta.querySelector('img');
    img.style.visibility = 'visible';
    carta.classList.add('flipped');
    cartasVolteadas.push(carta);

    // cuando hay dos cartas, esperar un poco y verificar
    if (cartasVolteadas.length === 2) {
        bloqueado = true;
        setTimeout(() => {
            verificarPareja();
            bloqueado = false;
        }, 500);
    }
}


function verificarPareja() {
    const [c1, c2] = cartasVolteadas;
    const img1 = c1.querySelector('img');
    const img2 = c2.querySelector('img');

    if (c1.dataset.simbolo === c2.dataset.simbolo) {
        // ✅ Coincidencia: se quedan verdes
        c1.classList.add('matched');
        c2.classList.add('matched');
        img1.style.visibility = 'visible';
        img2.style.visibility = 'visible';
        audioMatch.currentTime = 0;
        audioMatch.play();
    } else {
        // ❌ Error: se ponen rojas un instante
        c1.classList.add('error');
        c2.classList.add('error');

        setTimeout(() => {
            c1.classList.remove('error', 'flipped');
            c2.classList.remove('error', 'flipped');
            img1.style.visibility = 'hidden';
            img2.style.visibility = 'hidden';
        }, 600);

        intentos--;
        intentosSpan.textContent = intentos;

        if (intentos <= 0) {
            clearInterval(cuentaRegresiva);
            audioMain.pause();
            audioMain.currentTime = 0;
            registrarResultado("derrota", tiempo);
            audioLose.play();
            modalLose.show();
        }
    }


    cartasVolteadas = [];
    // Verificar victoria
    const todas = document.querySelectorAll('.memory-card');
    const ganadas = document.querySelectorAll('.matched');
    if (ganadas.length === todas.length) {
        clearInterval(cuentaRegresiva);
        audioMain.pause();
        audioMain.currentTime = 0;
        registrarResultado("victoria", tiempo);
        audioWin.play();
        modalWin.show();
    }
}


function registrarResultado(resultado, tiempoRestante) {
    fetch("/registrar-partida/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            nivel: nivel,
            resultado: resultado,
            tiempo_restante: tiempoRestante,
        }),
    }).catch(() => { });
}