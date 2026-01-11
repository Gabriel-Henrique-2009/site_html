const botaoTema = document.getElementById('tema');
const body = document.body;

botaoTema.addEventListener('click', () => {
    body.classList.toggle('modo-escuro');
    
    if (body.classList.contains('modo-escuro')) {
        botaoTema.textContent = 'tema - claro';
    } else {
        botaoTema.textContent = 'tema - escuro';
    }
});