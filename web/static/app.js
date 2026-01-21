// Exam Generator Web Interface - JavaScript

// ==================== UTILIDADES ====================

const API_BASE = "/api";

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

async function apiCall(method, endpoint, data = null) {
    try {
        const options = {
            method,
            headers: {
                "Content-Type": "application/json"
            }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Error en API");
        }
        return await response.json();
    } catch (error) {
        showToast(error.message, "error");
        throw error;
    }
}

function showTab(tabName) {
    // Ocultar todos
    document.querySelectorAll(".tab").forEach(tab => {
        tab.style.display = "none";
    });
    // Mostrar el seleccionado
    const tab = document.getElementById(`${tabName}-tab`);
    if (tab) {
        tab.style.display = "block";
        // Cargar contenido
        if (tabName === "list") loadProblems();
        if (tabName === "stats") loadStats();
    }
}

function createSpinner() {
    const div = document.createElement("div");
    div.className = "spinner";
    return div;
}

// ==================== TAB: LISTAR ====================

async function loadProblems() {
    const container = document.getElementById("problems-list");
    container.innerHTML = "";
    container.appendChild(createSpinner());
    
    try {
        const data = await apiCall("GET", "/problems");
        container.innerHTML = "";
        
        if (data.problems.length === 0) {
            container.innerHTML = "<p class='text-center'>No hay problemas</p>";
            return;
        }
        
        const grid = document.createElement("div");
        grid.className = "problems-grid";
        
        data.problems.forEach(problem => {
            const card = createProblemCard(problem);
            grid.appendChild(card);
        });
        
        container.appendChild(grid);
    } catch (error) {
        container.innerHTML = `<p class='error'>Error al cargar problemas</p>`;
    }
}

function createProblemCard(problem) {
    const card = document.createElement("div");
    card.className = "problem-card";
    
    const title = problem.metadata?.title || problem.id;
    const type = problem.type || "desconocido";
    const difficulty = problem.metadata?.difficulty || "-";
    const topic = problem.metadata?.topic || "-";
    
    card.innerHTML = `
        <h3>${title}</h3>
        <p>${problem.statement?.text || ""}</p>
        <div class="meta">
            <span class="badge type">${type}</span>
            <span class="badge difficulty">Dificultad: ${difficulty}</span>
        </div>
        <p style="font-size: 0.85rem; color: #7f8c8d; margin-top: 1rem;">
            Tema: ${topic}
        </p>
        <div style="margin-top: 1rem;">
            <button onclick="viewProblem('${problem.id}')" style="width: 48%; margin-right: 2%;">Ver</button>
            <button onclick="deleteProblem('${problem.id}')" class="danger" style="width: 48%;">Borrar</button>
        </div>
    `;
    
    return card;
}

async function viewProblem(problemId) {
    try {
        const data = await apiCall("GET", `/problems/${problemId}`);
        const problem = data.problem;
        
        alert(`
ID: ${problem.id}
Tipo: ${problem.type}
Título: ${problem.metadata.title}
Dificultad: ${problem.metadata.difficulty}
Tema: ${problem.metadata.topic}
Etiquetas: ${problem.metadata.tags.join(", ")}

Enunciado:
${problem.statement.text}

Solución:
${problem.solution.explanation}
        `);
    } catch (error) {
        // Error ya mostrado en toast
    }
}

async function deleteProblem(problemId) {
    if (confirm("¿Eliminar este problema?")) {
        try {
            await apiCall("DELETE", `/problems/${problemId}?confirm=true`);
            showToast("Problema eliminado", "success");
            loadProblems();
        } catch (error) {
            // Error ya mostrado en toast
        }
    }
}

// ==================== TAB: BÚSQUEDA ====================

async function search() {
    const query = document.getElementById("search-input").value;
    if (!query) {
        showToast("Ingresa una búsqueda", "warning");
        return;
    }
    
    const resultsDiv = document.getElementById("search-results");
    resultsDiv.innerHTML = "";
    resultsDiv.appendChild(createSpinner());
    
    try {
        const data = await apiCall("GET", `/search?q=${encodeURIComponent(query)}`);
        resultsDiv.innerHTML = "";
        
        if (data.results.length === 0) {
            resultsDiv.innerHTML = "<p class='text-center'>No se encontraron resultados</p>";
            return;
        }
        
        const grid = document.createElement("div");
        grid.className = "problems-grid";
        
        data.results.forEach(problem => {
            const card = createProblemCard(problem);
            grid.appendChild(card);
        });
        
        resultsDiv.appendChild(grid);
    } catch (error) {
        resultsDiv.innerHTML = `<p class='error'>Error en búsqueda</p>`;
    }
}

// ==================== TAB: ESTADÍSTICAS ====================

async function loadStats() {
    const container = document.getElementById("stats-content");
    container.innerHTML = "";
    container.appendChild(createSpinner());
    
    try {
        const data = await apiCall("GET", "/stats");
        const stats = data.stats;
        
        container.innerHTML = "";
        
        const grid = document.createElement("div");
        grid.className = "stats-grid";
        
        // Total
        const totalCard = document.createElement("div");
        totalCard.className = "stat-card";
        totalCard.innerHTML = `
            <h3>Total de Problemas</h3>
            <div class="number">${stats.total || 0}</div>
        `;
        grid.appendChild(totalCard);
        
        // Por tipo
        if (stats.by_type) {
            Object.entries(stats.by_type).forEach(([type, count]) => {
                const card = document.createElement("div");
                card.className = "stat-card";
                card.style.background = "linear-gradient(135deg, #27ae60, #229954)";
                card.innerHTML = `
                    <h3>${type}</h3>
                    <div class="number">${count}</div>
                `;
                grid.appendChild(card);
            });
        }
        
        container.appendChild(grid);
        
        // Tabla de dificultades
        if (stats.by_difficulty) {
            const diffTable = document.createElement("div");
            diffTable.className = "mt-3";
            diffTable.innerHTML = "<h3>Por Dificultad</h3>";
            
            let html = "<table style='width: 100%; border-collapse: collapse;'>";
            html += "<tr><th style='border-bottom: 2px solid #ddd; padding: 0.5rem;'>Dificultad</th>";
            html += "<th style='border-bottom: 2px solid #ddd; padding: 0.5rem;'>Cantidad</th></tr>";
            
            Object.entries(stats.by_difficulty).forEach(([diff, count]) => {
                html += `<tr>
                    <td style='border-bottom: 1px solid #eee; padding: 0.5rem;'>${diff}</td>
                    <td style='border-bottom: 1px solid #eee; padding: 0.5rem;'>${count}</td>
                </tr>`;
            });
            
            html += "</table>";
            diffTable.innerHTML += html;
            container.appendChild(diffTable);
        }
    } catch (error) {
        container.innerHTML = `<p class='error'>Error al cargar estadísticas</p>`;
    }
}

// ==================== TAB: EXPORTAR ====================

async function exportJSON() {
    try {
        const response = await fetch(`${API_BASE}/export/json`);
        if (!response.ok) throw new Error("Error en descarga");
        
        const blob = await response.blob();
        downloadBlob(blob, `problems_${new Date().toISOString().split('T')[0]}.json`);
        showToast("Exportado a JSON", "success");
    } catch (error) {
        showToast("Error al exportar JSON", "error");
    }
}

async function exportCSV() {
    try {
        const response = await fetch(`${API_BASE}/export/csv`);
        if (!response.ok) throw new Error("Error en descarga");
        
        const blob = await response.blob();
        downloadBlob(blob, `problems_${new Date().toISOString().split('T')[0]}.csv`);
        showToast("Exportado a CSV", "success");
    } catch (error) {
        showToast("Error al exportar CSV", "error");
    }
}

function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// ==================== TAB: IMPORTAR ====================

async function importFile() {
    const fileInput = document.getElementById("import-file");
    if (!fileInput.files.length) {
        showToast("Selecciona un archivo", "warning");
        return;
    }
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    formData.append("skip_duplicates", "true");
    
    try {
        const response = await fetch(`${API_BASE}/import`, {
            method: "POST",
            body: formData
        });
        
        if (!response.ok) throw new Error("Error en importación");
        
        const data = await response.json();
        showToast(`Importados: ${data.imported}, Saltados: ${data.skipped}`, "success");
        fileInput.value = "";
        loadProblems();
    } catch (error) {
        showToast("Error al importar archivo", "error");
    }
}

// ==================== INICIALIZACIÓN ====================

document.addEventListener("DOMContentLoaded", () => {
    showTab("list");
    
    // Enter en búsqueda
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") search();
        });
    }
});
