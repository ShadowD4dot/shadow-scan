#!/usr/bin/env python3
"""
Shadow-Scan Dashboard - Panel Web Interactivo
Visualización de resultados de escaneos
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sqlite3
from collections import defaultdict

app = Flask(__name__)

class ScanDatabase:
    """Manejo de base de datos SQLite para histórico de escaneos"""
    
    def __init__(self, db_path: str = "scans.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar esquema de base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de escaneos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_subdomains INTEGER,
                total_alive_hosts INTEGER,
                total_vulnerabilities INTEGER,
                critical_count INTEGER,
                high_count INTEGER,
                medium_count INTEGER,
                report_path TEXT,
                status TEXT DEFAULT 'completed'
            )
        """)
        
        # Tabla de vulnerabilidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                severity TEXT,
                name TEXT,
                host TEXT,
                template_id TEXT,
                description TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_scan(self, scan_data: Dict) -> int:
        """Agregar nuevo escaneo a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = scan_data.get('statistics', {})
        vuln_severity = stats.get('vulnerability_severity', {})
        
        cursor.execute("""
            INSERT INTO scans 
            (target, timestamp, total_subdomains, total_alive_hosts, 
             total_vulnerabilities, critical_count, high_count, medium_count, report_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scan_data['scan_info']['target'],
            scan_data['scan_info']['timestamp'],
            stats.get('total_subdomains', 0),
            stats.get('total_alive_hosts', 0),
            stats.get('total_vulnerabilities', 0),
            vuln_severity.get('critical', 0),
            vuln_severity.get('high', 0),
            vuln_severity.get('medium', 0),
            scan_data['scan_info'].get('scan_directory', '')
        ))
        
        scan_id = cursor.lastrowid
        
        # Agregar vulnerabilidades
        for vuln in scan_data.get('vulnerabilities', []):
            info = vuln.get('info', {})
            cursor.execute("""
                INSERT INTO vulnerabilities 
                (scan_id, severity, name, host, template_id, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                scan_id,
                info.get('severity', 'unknown'),
                info.get('name', 'Unknown'),
                vuln.get('host', ''),
                vuln.get('template-id', ''),
                info.get('description', '')
            ))
        
        conn.commit()
        conn.close()
        
        return scan_id
    
    def get_all_scans(self) -> List[Dict]:
        """Obtener todos los escaneos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM scans 
            ORDER BY timestamp DESC
        """)
        
        scans = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return scans
    
    def get_scan(self, scan_id: int) -> Dict:
        """Obtener escaneo específico con vulnerabilidades"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
        scan = dict(cursor.fetchone())
        
        cursor.execute("""
            SELECT * FROM vulnerabilities 
            WHERE scan_id = ?
            ORDER BY 
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                    ELSE 5
                END
        """, (scan_id,))
        
        scan['vulnerabilities'] = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return scan
    
    def get_statistics(self) -> Dict:
        """Obtener estadísticas globales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_scans,
                SUM(total_vulnerabilities) as total_vulns,
                SUM(critical_count) as total_critical,
                SUM(high_count) as total_high
            FROM scans
        """)
        
        row = cursor.fetchone()
        stats = {
            'total_scans': row[0] or 0,
            'total_vulnerabilities': row[1] or 0,
            'critical_vulnerabilities': row[2] or 0,
            'high_vulnerabilities': row[3] or 0
        }
        
        conn.close()
        return stats


# Instancia global de base de datos
db = ScanDatabase()


@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('dashboard.html')


@app.route('/api/scans')
def api_scans():
    """API: Listar todos los escaneos"""
    scans = db.get_all_scans()
    return jsonify(scans)


@app.route('/api/scan/<int:scan_id>')
def api_scan(scan_id):
    """API: Obtener detalles de un escaneo"""
    scan = db.get_scan(scan_id)
    return jsonify(scan)


@app.route('/api/statistics')
def api_statistics():
    """API: Obtener estadísticas globales"""
    stats = db.get_statistics()
    return jsonify(stats)


@app.route('/api/import_scan', methods=['POST'])
def api_import_scan():
    """API: Importar escaneo desde archivo JSON"""
    try:
        if 'file' in request.files:
            file = request.files['file']
            scan_data = json.load(file)
        elif request.json:
            scan_data = request.json
        else:
            return jsonify({'error': 'No data provided'}), 400
        
        scan_id = db.add_scan(scan_data)
        return jsonify({'success': True, 'scan_id': scan_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/import_from_directory', methods=['POST'])
def api_import_from_directory():
    """API: Importar todos los escaneos de un directorio"""
    try:
        data = request.json
        scan_dir = Path(data.get('directory', 'scan_results'))
        
        imported = 0
        errors = []
        
        # Buscar todos los full_report.json
        for report_file in scan_dir.rglob('full_report.json'):
            try:
                with open(report_file) as f:
                    scan_data = json.load(f)
                db.add_scan(scan_data)
                imported += 1
            except Exception as e:
                errors.append(f"{report_file}: {str(e)}")
        
        return jsonify({
            'success': True,
            'imported': imported,
            'errors': errors
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_html_template():
    """Crear template HTML del dashboard"""
    template_dir = Path("templates")
    template_dir.mkdir(exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow-Scan Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .severity-critical { background-color: #ef4444; }
        .severity-high { background-color: #f97316; }
        .severity-medium { background-color: #eab308; }
        .severity-low { background-color: #22c55e; }
        .severity-info { background-color: #6b7280; }
    </style>
</head>
<body class="bg-gray-900 text-gray-100">
    
    <!-- Header -->
    <nav class="bg-gray-800 border-b border-gray-700">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <h1 class="text-2xl font-bold text-white">🕵️ Shadow-Scan Dashboard</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="importScans()" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">
                        📥 Importar Escaneos
                    </button>
                    <button onclick="refreshData()" class="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg">
                        🔄 Actualizar
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="text-gray-400 text-sm mb-2">Total Escaneos</div>
                <div id="stat-scans" class="text-3xl font-bold">0</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="text-gray-400 text-sm mb-2">Vulnerabilidades</div>
                <div id="stat-vulns" class="text-3xl font-bold">0</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border border-red-900">
                <div class="text-gray-400 text-sm mb-2">🔴 Críticas</div>
                <div id="stat-critical" class="text-3xl font-bold text-red-500">0</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border border-orange-900">
                <div class="text-gray-400 text-sm mb-2">🟠 Altas</div>
                <div id="stat-high" class="text-3xl font-bold text-orange-500">0</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 class="text-lg font-semibold mb-4">Vulnerabilidades por Severidad</h3>
                <canvas id="severityChart"></canvas>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 class="text-lg font-semibold mb-4">Timeline de Escaneos</h3>
                <canvas id="timelineChart"></canvas>
            </div>
        </div>

        <!-- Scans List -->
        <div class="bg-gray-800 rounded-lg border border-gray-700">
            <div class="px-6 py-4 border-b border-gray-700">
                <h3 class="text-lg font-semibold">📊 Historial de Escaneos</h3>
            </div>
            <div id="scans-list" class="divide-y divide-gray-700">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <!-- Scan Details Modal -->
    <div id="scan-modal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
        <div class="bg-gray-800 rounded-lg max-w-4xl w-full max-h-screen overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-start mb-6">
                    <h2 id="modal-title" class="text-2xl font-bold">Detalles del Escaneo</h2>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-white">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div id="modal-content">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>
    </div>

    <script>
        let scansData = [];
        let severityChart = null;
        let timelineChart = null;

        // Load data on page load
        window.onload = function() {
            loadStatistics();
            loadScans();
        };

        async function loadStatistics() {
            try {
                const response = await fetch('/api/statistics');
                const stats = await response.json();
                
                document.getElementById('stat-scans').textContent = stats.total_scans;
                document.getElementById('stat-vulns').textContent = stats.total_vulnerabilities;
                document.getElementById('stat-critical').textContent = stats.critical_vulnerabilities;
                document.getElementById('stat-high').textContent = stats.high_vulnerabilities;
            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        }

        async function loadScans() {
            try {
                const response = await fetch('/api/scans');
                scansData = await response.json();
                
                renderScansList();
                updateCharts();
            } catch (error) {
                console.error('Error loading scans:', error);
            }
        }

        function renderScansList() {
            const container = document.getElementById('scans-list');
            
            if (scansData.length === 0) {
                container.innerHTML = '<div class="p-6 text-gray-400 text-center">No hay escaneos disponibles</div>';
                return;
            }
            
            container.innerHTML = scansData.map(scan => `
                <div class="p-6 hover:bg-gray-750 cursor-pointer transition" onclick="showScanDetails(${scan.id})">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="flex items-center space-x-3 mb-2">
                                <h4 class="text-lg font-semibold">${scan.target}</h4>
                                <span class="text-sm text-gray-400">${new Date(scan.timestamp).toLocaleString()}</span>
                            </div>
                            <div class="flex space-x-6 text-sm">
                                <span class="text-gray-400">🌐 ${scan.total_subdomains} subdominios</span>
                                <span class="text-gray-400">✅ ${scan.total_alive_hosts} hosts activos</span>
                                <span class="text-gray-400">🎯 ${scan.total_vulnerabilities} vulnerabilidades</span>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            ${scan.critical_count > 0 ? `<span class="severity-critical text-white text-xs px-2 py-1 rounded">${scan.critical_count} CRITICAL</span>` : ''}
                            ${scan.high_count > 0 ? `<span class="severity-high text-white text-xs px-2 py-1 rounded">${scan.high_count} HIGH</span>` : ''}
                            ${scan.medium_count > 0 ? `<span class="severity-medium text-white text-xs px-2 py-1 rounded">${scan.medium_count} MEDIUM</span>` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        async function showScanDetails(scanId) {
            try {
                const response = await fetch(`/api/scan/${scanId}`);
                const scan = await response.json();
                
                document.getElementById('modal-title').textContent = `Escaneo: ${scan.target}`;
                
                const content = document.getElementById('modal-content');
                content.innerHTML = `
                    <div class="space-y-6">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <span class="text-gray-400">Target:</span>
                                <span class="ml-2 font-mono">${scan.target}</span>
                            </div>
                            <div>
                                <span class="text-gray-400">Fecha:</span>
                                <span class="ml-2">${new Date(scan.timestamp).toLocaleString()}</span>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="text-lg font-semibold mb-4">🎯 Vulnerabilidades (${scan.vulnerabilities.length})</h3>
                            <div class="space-y-4 max-h-96 overflow-y-auto">
                                ${scan.vulnerabilities.length === 0 ? 
                                    '<p class="text-gray-400">No se detectaron vulnerabilidades</p>' :
                                    scan.vulnerabilities.map(vuln => `
                                        <div class="bg-gray-900 p-4 rounded-lg border border-gray-700">
                                            <div class="flex justify-between items-start mb-2">
                                                <h4 class="font-semibold">${vuln.name}</h4>
                                                <span class="severity-${vuln.severity} text-white text-xs px-2 py-1 rounded">
                                                    ${vuln.severity.toUpperCase()}
                                                </span>
                                            </div>
                                            <div class="text-sm text-gray-400 mb-2">
                                                🌐 ${vuln.host}
                                            </div>
                                            ${vuln.description ? `<p class="text-sm text-gray-300">${vuln.description}</p>` : ''}
                                        </div>
                                    `).join('')
                                }
                            </div>
                        </div>
                    </div>
                `;
                
                document.getElementById('scan-modal').classList.remove('hidden');
            } catch (error) {
                console.error('Error loading scan details:', error);
            }
        }

        function closeModal() {
            document.getElementById('scan-modal').classList.add('hidden');
        }

        function updateCharts() {
            // Severity Chart
            const severityCounts = {critical: 0, high: 0, medium: 0, low: 0};
            scansData.forEach(scan => {
                severityCounts.critical += scan.critical_count || 0;
                severityCounts.high += scan.high_count || 0;
                severityCounts.medium += scan.medium_count || 0;
            });

            if (severityChart) severityChart.destroy();
            
            const ctxSeverity = document.getElementById('severityChart').getContext('2d');
            severityChart = new Chart(ctxSeverity, {
                type: 'doughnut',
                data: {
                    labels: ['Critical', 'High', 'Medium'],
                    datasets: [{
                        data: [severityCounts.critical, severityCounts.high, severityCounts.medium],
                        backgroundColor: ['#ef4444', '#f97316', '#eab308']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#fff' } }
                    }
                }
            });

            // Timeline Chart
            const timelineData = scansData.slice(0, 10).reverse().map(scan => ({
                x: new Date(scan.timestamp).toLocaleDateString(),
                y: scan.total_vulnerabilities
            }));

            if (timelineChart) timelineChart.destroy();
            
            const ctxTimeline = document.getElementById('timelineChart').getContext('2d');
            timelineChart = new Chart(ctxTimeline, {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Vulnerabilidades',
                        data: timelineData,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { ticks: { color: '#fff' }, grid: { color: '#374151' } },
                        y: { ticks: { color: '#fff' }, grid: { color: '#374151' } }
                    },
                    plugins: {
                        legend: { labels: { color: '#fff' } }
                    }
                }
            });
        }

        async function importScans() {
            const directory = prompt('Ingresa el directorio de escaneos:', 'scan_results');
            if (!directory) return;
            
            try {
                const response = await fetch('/api/import_from_directory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ directory })
                });
                
                const result = await response.json();
                alert(`✅ Importados ${result.imported} escaneos`);
                refreshData();
            } catch (error) {
                alert('❌ Error importando escaneos: ' + error);
            }
        }

        function refreshData() {
            loadStatistics();
            loadScans();
        }
    </script>
</body>
</html>"""
    
    with open(template_dir / "dashboard.html", "w") as f:
        f.write(html_content)
    
    print("✅ Template HTML creado")


if __name__ == "__main__":
    create_html_template()
    print("\n🚀 Iniciando Shadow-Scan Dashboard...")
    print("📍 Accede en: http://localhost:5000")
    print("\n💡 Para importar escaneos:")
    print("   1. Abre el dashboard en tu navegador")
    print("   2. Haz clic en 'Importar Escaneos'")
    print("   3. Ingresa el directorio 'scan_results'\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
