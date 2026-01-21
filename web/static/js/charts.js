/**
 * Chart.js Integration for GeneratorFEExercises
 * Handles creation and management of interactive charts
 */

// Global chart instance
let distributionChart = null;

/**
 * Toggle visibility of fixed-point and floating-point controls
 */
function toggleControls() {
    const numType = document.getElementById('numType').value;
    const fixedPointControls = document.getElementById('fixedPointControls');
    const floatingPointControls = document.getElementById('floatingPointControls');
    
    if (numType === 'fixed_point') {
        fixedPointControls.style.display = 'block';
        floatingPointControls.style.display = 'none';
    } else {
        fixedPointControls.style.display = 'none';
        floatingPointControls.style.display = 'block';
    }
}

/**
 * Crear gráfica de distribución con Chart.js
 */
async function analyzeDistribution() {
    const numType = document.getElementById('numType').value;
    const base = parseInt(document.getElementById('base').value);
    
    // Validar base
    if (base < 2 || base > 36 || isNaN(base)) {
        alert('❌ Base inválida. Debe ser un número entre 2 y 36.');
        return;
    }
    
    let payload;
    
    if (numType === 'fixed_point') {
        const E = parseInt(document.getElementById('E').value);
        const F = parseInt(document.getElementById('F').value);
        const representation = document.getElementById('representation').value;
        
        payload = { E, F, representation, base, tipo_numero: 'fixed_point' };
    } else {
        const E_fp = parseInt(document.getElementById('E_fp').value);
        const F_fp = parseInt(document.getElementById('F_fp').value);
        
        payload = { E: E_fp, F: F_fp, base, tipo_numero: 'floating_point' };
    }
    
    try {
        // Mostrar estado de carga
        const statsDiv = document.getElementById('stats');
        statsDiv.innerHTML = '<p style="text-align: center; color: #666;">⏳ Analizando distribución...</p>';
        
        // Llamar API para obtener datos de gráfica
        const response = await fetch('/api/distribution/chart-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Error desconocido');
        }
        
        // Mostrar estadísticas
        const stats = result.statistics;
        statsDiv.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
                <div class="stat-box">
                    <label>Mín. Valor:</label>
                    <span>${stats.min.toFixed(6)}</span>
                </div>
                <div class="stat-box">
                    <label>Máx. Valor:</label>
                    <span>${stats.max.toFixed(6)}</span>
                </div>
                <div class="stat-box">
                    <label>Epsilon (Brecha):</label>
                    <span>${stats.epsilon.toFixed(6)}</span>
                </div>
                <div class="stat-box">
                    <label>Total Bits:</label>
                    <span>${stats.total_bits}</span>
                </div>
                <div class="stat-box">
                    <label>Total Números:</label>
                    <span>${stats.total_numbers.toLocaleString()}</span>
                </div>
                <div class="stat-box">
                    <label>Tipo:</label>
                    <span>${stats.gap_type}</span>
                </div>
            </div>
        `;
        
        // Crear contenedor de gráfica si no existe
        let chartContainer = document.getElementById('chartContainer');
        if (!chartContainer) {
            const chartsDiv = document.getElementById('charts');
            chartsDiv.innerHTML = `
                <div id="chartContainer" style="position: relative; height: 400px; margin-top: 30px;">
                    <canvas id="distributionCanvas"></canvas>
                </div>
            `;
            chartContainer = document.getElementById('chartContainer');
        }
        
        // Destruir gráfica anterior si existe
        if (distributionChart) {
            distributionChart.destroy();
        }
        
        // Crear nueva gráfica
        const canvas = document.getElementById('distributionCanvas');
        const ctx = canvas.getContext('2d');
        
        distributionChart = new Chart(ctx, {
            type: result.chart_type,
            data: {
                labels: result.labels,
                datasets: result.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: numType === 'fixed_point' 
                            ? `Distribución de Números en Punto Fijo (E=${payload.E}, F=${payload.F}, Base=${base})` 
                            : `Distribución de Números en IEEE754 (E=${payload.E}, F=${payload.F}, Base=${base})`,
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Frecuencia: ${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Frecuencia'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Rango de Valores'
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('stats').innerHTML = `
            <div style="padding: 15px; background-color: #fee; border: 1px solid #fcc; border-radius: 4px; color: #c33;">
                ❌ Error: ${error.message}
            </div>
        `;
    }
}

/**
 * Limpiar gráfica
 */
function resetDistribution() {
    // Limpiar inputs
    document.getElementById('E').value = '4';
    document.getElementById('F').value = '4';
    document.getElementById('representation').value = 'unsigned';
    document.getElementById('base').value = '2';
    document.getElementById('E_fp').value = '8';
    document.getElementById('F_fp').value = '23';
    document.getElementById('numType').value = 'fixed_point';
    toggleControls();
    
    // Limpiar gráfica
    if (distributionChart) {
        distributionChart.destroy();
        distributionChart = null;
    }
    
    // Limpiar estadísticas
    document.getElementById('stats').innerHTML = '';
    
    // Limpiar contenedor de gráfica si existe
    const chartContainer = document.getElementById('chartContainer');
    if (chartContainer) {
        chartContainer.remove();
    }
}

/**
 * Exportar gráfica como PNG
 */
function exportChart() {
    if (!distributionChart) {
        alert('⚠️ No hay gráfica para exportar. Analiza una distribución primero.');
        return;
    }
    
    try {
        const image = distributionChart.toBase64Image();
        const link = document.createElement('a');
        link.href = image;
        link.download = `distribution_${new Date().getTime()}.png`;
        link.click();
    } catch (error) {
        console.error('Error exportando gráfica:', error);
        alert('❌ Error al exportar la gráfica');
    }
}

/**
 * Cambiar tipo de gráfica (dinámicamente)
 */
function changeChartType(type) {
    if (!distributionChart) {
        alert('⚠️ No hay datos para cambiar. Analiza una distribución primero.');
        return;
    }
    
    distributionChart.config.type = type;
    distributionChart.update();
}

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    // Agregar event listeners a botones si existen
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeDistribution);
    }
    
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetDistribution);
    }
    
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportChart);
    }
});
