/**
 * Dark Mode Toggle
 * Maneja el cambio entre tema claro y oscuro
 */

const DARK_MODE_KEY = 'darkMode';

/**
 * Inicializar tema oscuro
 */
function initDarkMode() {
    // Obtener preferencia guardada o detectar preferencia del sistema
    const isDarkMode = localStorage.getItem(DARK_MODE_KEY) === 'true' ||
                       (!localStorage.getItem(DARK_MODE_KEY) && 
                        window.matchMedia && 
                        window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    if (isDarkMode) {
        enableDarkMode();
    }
}

/**
 * Habilitar modo oscuro
 */
function enableDarkMode() {
    document.body.classList.add('dark-mode');
    localStorage.setItem(DARK_MODE_KEY, 'true');
    updateDarkModeToggle();
}

/**
 * Deshabilitar modo oscuro
 */
function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    localStorage.setItem(DARK_MODE_KEY, 'false');
    updateDarkModeToggle();
}

/**
 * Alternar modo oscuro
 */
function toggleDarkMode() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    if (isDarkMode) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
}

/**
 * Actualizar icono del toggle
 */
function updateDarkModeToggle() {
    const toggle = document.querySelector('.dark-mode-toggle');
    if (!toggle) return;
    
    const isDarkMode = document.body.classList.contains('dark-mode');
    toggle.textContent = isDarkMode ? '☀️' : '🌙';
    toggle.title = isDarkMode ? 'Modo Claro' : 'Modo Oscuro';
}

/**
 * Crear botón de toggle de modo oscuro
 */
function createDarkModeToggle() {
    // No crear si ya existe
    if (document.querySelector('.dark-mode-toggle')) {
        return;
    }
    
    const toggle = document.createElement('button');
    toggle.className = 'dark-mode-toggle';
    toggle.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    toggle.title = document.body.classList.contains('dark-mode') ? 'Modo Claro' : 'Modo Oscuro';
    toggle.onclick = toggleDarkMode;
    
    document.body.appendChild(toggle);
}

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
    createDarkModeToggle();
});

// Escuchar cambios en preferencias del sistema
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem(DARK_MODE_KEY)) {
            if (e.matches) {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        }
    });
}
