"""
FASE D: CLI Tools para gestión de problemas.

Proporciona interfaz de línea de comandos para:
- Listar y buscar problemas
- Ver estadísticas
- Exportar e importar
- Backup y restore
- Validación de integridad

Uso:
    python -m cli.problems list --type numeracion --difficulty 3
    python -m cli.problems search "conversión"
    python -m cli.problems stats
    python -m cli.problems export --format json --output problems.json
    python -m cli.problems backup
    python -m cli.problems restore backup_20260115.zip
"""

import json
import os
import shutil
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys

# Importar repositorio
from database import FileProblemRepository, SQLiteProblemRepository, ProblemRepository
from models.problem_type import ProblemType


class ProblemsCLI:
    """Interface CLI para gestión de problemas."""
    
    def __init__(self, repo_or_path=None, backend: str = "file"):
        """
        Inicializa ProblemsCLI.
        
        Args:
            repo_or_path: Objeto ProblemRepository o ruta del repositorio (str)
            backend: "file" o "sqlite" (solo si repo_or_path es string)
        """
        # Si se pasa un objeto repository, usarlo directamente
        if isinstance(repo_or_path, ProblemRepository):
            self.repo = repo_or_path
            self.repo_path = "memory"
            self.backend = "custom"
        else:
            # Si no se pasa nada, usar por defecto
            if repo_or_path is None:
                repo_or_path = "./problems"
            
            self.repo_path = repo_or_path
            self.backend = backend.lower()
            
            # Crear repositorio según backend
            if self.backend == "sqlite":
                self.repo = SQLiteProblemRepository(f"{repo_or_path}.db")
            else:
                self.repo = FileProblemRepository(repo_or_path)
    
    # ==================== LIST ====================
    
    def list(self, 
             type_filter: Optional[str] = None,
             difficulty: Optional[int] = None,
             tag: Optional[str] = None,
             limit: int = 10,
             offset: int = 0,
             verbose: bool = False):
        """
        Lista problemas con filtros opcionales.
        
        Args:
            type_filter: Filtrar por tipo (numeracion, karnaugh, etc)
            difficulty: Filtrar por dificultad (1-5)
            tag: Filtrar por tag
            limit: Máximo de resultados
            offset: Saltar N resultados
            verbose: Mostrar detalles completos
        """
        # Construir filtros
        filters = {}
        if type_filter:
            filters['type'] = type_filter
        if difficulty:
            filters['difficulty'] = difficulty
        if tag:
            filters['tags'] = [tag]
        filters['limit'] = limit
        filters['offset'] = offset
        
        # Listar
        problems = self.repo.list(filters)
        
        if not problems:
            print(f"[INFO] No se encontraron problemas")
            return
        
        print(f"\n[RESULTS] {len(problems)} problema(s) encontrado(s)")
        print("=" * 100)
        
        for i, problem in enumerate(problems, 1):
            self._print_problem_summary(problem, i, verbose)
        
        print("=" * 100)
        info = self.repo.info()
        print(f"[INFO] Total en BD: {info['total']} | Mostrando {offset+1}-{offset+len(problems)}")
    
    def _print_problem_summary(self, problem, index: int, verbose: bool = False):
        """Imprime resumen de un problema."""
        print(f"\n{index}. {problem.metadata.title} (ID: {problem.id[:8]}...)")
        print(f"   Tipo: {problem.type.value if problem.type else 'N/A'}")
        print(f"   Dificultad: {problem.metadata.difficulty}/5")
        print(f"   Creado: {problem.metadata.created_at}")
        
        if problem.metadata.tags:
            print(f"   Tags: {', '.join(problem.metadata.tags)}")
        
        if verbose:
            print(f"   Enunciado: {problem.statement.text[:100]}..." if len(problem.statement.text) > 100 else f"   Enunciado: {problem.statement.text}")
            if problem.solution.explanation:
                print(f"   Explicación: {problem.solution.explanation[:100]}...")
    
    # ==================== SEARCH ====================
    
    def search(self, query: str, limit: int = 10, verbose: bool = False):
        """
        Busca problemas por texto.
        
        Args:
            query: Texto a buscar (en título, enunciado, etc)
            limit: Máximo de resultados
            verbose: Mostrar detalles
        """
        query_lower = query.lower()
        results = []
        
        # Buscar en todos los problemas
        all_problems = self.repo.list({'limit': 1000})
        
        for problem in all_problems:
            # Buscar en título
            if query_lower in problem.metadata.title.lower():
                results.append((problem, "título"))
                continue
            
            # Buscar en enunciado
            if query_lower in problem.statement.text.lower():
                results.append((problem, "enunciado"))
                continue
            
            # Buscar en tags
            if any(query_lower in tag.lower() for tag in problem.metadata.tags):
                results.append((problem, "tag"))
        
        if not results:
            print(f"[INFO] No se encontraron problemas con '{query}'")
            return
        
        print(f"\n[RESULTS] {len(results[:limit])} resultado(s) para '{query}'")
        print("=" * 100)
        
        for i, (problem, match_type) in enumerate(results[:limit], 1):
            self._print_problem_summary(problem, i, verbose)
            print(f"   Match: {match_type}")
        
        print("=" * 100)
    
    # ==================== STATS ====================
    
    def stats(self, detailed: bool = False):
        """
        Muestra estadísticas del repositorio.
        
        Args:
            detailed: Mostrar estadísticas detalladas por tipo/dificultad
        """
        info = self.repo.info()
        
        print("\n" + "=" * 70)
        print("ESTADÍSTICAS DEL REPOSITORIO".center(70))
        print("=" * 70)
        
        print(f"\nBackend: {info['backend']}")
        print(f"Ubicación: {info['location']}")
        print(f"Total de problemas: {info['total']}")
        print(f"Tamaño: {info['size_mb']:.2f} MB")
        
        if detailed and info['total'] > 0:
            print(f"\nPor tipo:")
            for problem_type, count in info.get('by_type', {}).items():
                percentage = (count / info['total'] * 100) if info['total'] > 0 else 0
                print(f"   {problem_type}: {count} ({percentage:.1f}%)")
            
            print(f"\nPor dificultad:")
            for difficulty in range(1, 6):
                count = info.get('by_difficulty', {}).get(difficulty, 0)
                if count > 0:
                    percentage = (count / info['total'] * 100)
                    stars = "★" * difficulty + "☆" * (5 - difficulty)
                    print(f"   {stars} ({difficulty}): {count} ({percentage:.1f}%)")
        
        print("=" * 70 + "\n")
    
    # ==================== EXPORT ====================
    
    def export(self, output_file: str, format: str = "json", type_filter: Optional[str] = None):
        """
        Exporta problemas a archivo.
        
        Args:
            output_file: Ruta del archivo de salida
            format: Formato (json, csv)
            type_filter: Filtrar por tipo
        """
        filters = {}
        if type_filter:
            filters['type'] = type_filter
        
        problems = self.repo.list(filters)
        
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        
        if format.lower() == "json":
            self._export_json(problems, output_file)
        elif format.lower() == "csv":
            self._export_csv(problems, output_file)
        else:
            print(f"[ERROR] Formato no soportado: {format}")
    
    def _export_json(self, problems, output_file: str):
        """Exporta a JSON."""
        data = {
            "export_date": datetime.now().isoformat(),
            "total": len(problems),
            "problems": [p.to_dict() for p in problems]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Exportado: {output_file} ({len(problems)} problemas)")
    
    def _export_csv(self, problems, output_file: str):
        """Exporta a CSV."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Encabezados
            writer.writerow([
                'ID', 'Tipo', 'Dificultad', 'Título', 
                'Tags', 'Creado', 'Actualizado'
            ])
            
            # Datos
            for p in problems:
                writer.writerow([
                    p.id,
                    p.type.value if p.type else "",
                    p.metadata.difficulty,
                    p.metadata.title,
                    "|".join(p.metadata.tags),
                    p.metadata.created_at,
                    p.metadata.updated_at
                ])
        
        print(f"[OK] Exportado: {output_file} ({len(problems)} problemas)")
    
    # ==================== IMPORT ====================
    
    def import_from_file(self, input_file: str, format: str = "json", skip_duplicates: bool = True):
        """
        Importa problemas desde archivo.
        
        Args:
            input_file: Ruta del archivo a importar
            format: Formato (json)
            skip_duplicates: Saltar problemas que ya existen
        """
        if format.lower() != "json":
            print(f"[ERROR] Formato no soportado: {format}")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        problems_data = data if isinstance(data, list) else data.get('problems', [])
        
        imported = 0
        skipped = 0
        
        from models.problem import Problem
        
        for p_data in problems_data:
            problem_id = p_data.get('id')
            
            if skip_duplicates and self.repo.exists(problem_id):
                skipped += 1
                continue
            
            problem = Problem.from_dict(p_data)
            self.repo.save(problem)
            imported += 1
        
        print(f"[OK] Importado: {imported} nuevos, {skipped} duplicados saltados")
    
    # ==================== DELETE ====================
    
    def delete(self, problem_id: str, confirm: bool = False):
        """
        Elimina un problema.
        
        Args:
            problem_id: ID del problema a eliminar
            confirm: Confirmar sin preguntar
        """
        if not self.repo.exists(problem_id):
            print(f"[ERROR] Problema no encontrado: {problem_id}")
            return
        
        if not confirm:
            problem = self.repo.load(problem_id)
            print(f"Eliminar: {problem.metadata.title} ({problem_id[:8]}...)?")
            if input("Confirmar (s/n): ").lower() != 's':
                print("[CANCELLED]")
                return
        
        self.repo.delete(problem_id)
        print(f"[OK] Eliminado: {problem_id}")
    
    def delete_by_filter(self, type_filter: Optional[str] = None, 
                        difficulty: Optional[int] = None, confirm: bool = False):
        """Elimina múltiples problemas por filtro."""
        filters = {}
        if type_filter:
            filters['type'] = type_filter
        if difficulty:
            filters['difficulty'] = difficulty
        
        problems = self.repo.list(filters)
        
        if not problems:
            print(f"[INFO] No hay problemas que cumplan los criterios")
            return
        
        print(f"[WARN] Se van a eliminar {len(problems)} problema(s)")
        for p in problems[:5]:
            print(f"   - {p.metadata.title}")
        if len(problems) > 5:
            print(f"   ... y {len(problems) - 5} más")
        
        if not confirm:
            if input("Confirmar eliminación (s/n): ").lower() != 's':
                print("[CANCELLED]")
                return
        
        deleted = 0
        for p in problems:
            self.repo.delete(p.id)
            deleted += 1
        
        print(f"[OK] Eliminados: {deleted} problemas")
    
    # ==================== BACKUP ====================
    
    def backup(self, output_dir: str = "./backups"):
        """
        Crea backup del repositorio.
        
        Args:
            output_dir: Directorio para guardar backups
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(output_dir, backup_name)
        
        if self.backend == "sqlite":
            # Copiar archivo DB
            db_file = f"{self.repo_path}.db"
            shutil.copy(db_file, f"{backup_path}.db")
            print(f"[OK] Backup creado: {backup_path}.db")
        else:
            # Copiar directorio
            shutil.copytree(self.repo_path, backup_path)
            print(f"[OK] Backup creado: {backup_path}")
    
    # ==================== RESTORE ====================
    
    def restore(self, backup_path: str, confirm: bool = False):
        """
        Restaura repositorio desde backup.
        
        Args:
            backup_path: Ruta del backup
            confirm: Confirmar sin preguntar
        """
        if not os.path.exists(backup_path):
            print(f"[ERROR] Backup no encontrado: {backup_path}")
            return
        
        print(f"[WARN] Esto sobrescribirá el repositorio actual")
        if not confirm:
            if input("Confirmar restauración (s/n): ").lower() != 's':
                print("[CANCELLED]")
                return
        
        if backup_path.endswith('.db'):
            # Restaurar DB
            db_file = f"{self.repo_path}.db"
            shutil.copy(backup_path, db_file)
            print(f"[OK] Restaurado: {db_file}")
        else:
            # Restaurar directorio
            if os.path.exists(self.repo_path):
                shutil.rmtree(self.repo_path)
            shutil.copytree(backup_path, self.repo_path)
            print(f"[OK] Restaurado: {self.repo_path}")
    
    # ==================== VERIFY ====================
    
    def verify(self, repair: bool = False):
        """
        Verifica integridad del repositorio.
        
        Args:
            repair: Intentar reparar problemas encontrados
        """
        print("\n[CHECK] Verificando integridad...")
        
        issues = []
        info = self.repo.info()
        
        # Check 1: Total debe ser > 0
        if info['total'] == 0:
            print("[WARN] Repositorio vacío")
            return
        
        # Check 2: Cargar cada problema
        all_problems = self.repo.list({'limit': 1000})
        corrupted = []
        
        for problem in all_problems:
            try:
                # Verificar campos esenciales
                assert problem.id
                assert problem.type
                assert problem.metadata.title
                assert problem.statement.text
            except AssertionError:
                corrupted.append(problem.id)
        
        if corrupted:
            issues.append(f"Problemas corruptos: {len(corrupted)}")
            for pid in corrupted[:5]:
                print(f"   - {pid}")
            if len(corrupted) > 5:
                print(f"   ... y {len(corrupted) - 5} más")
            
            if repair:
                for pid in corrupted:
                    self.repo.delete(pid)
                print(f"[OK] Reparado: eliminados {len(corrupted)} problemas corruptos")
        
        if not issues:
            print(f"[OK] Integridad verificada: {info['total']} problemas OK")
        else:
            print(f"[ERROR] Se encontraron {len(issues)} problema(s)")


def main():
    """Punto de entrada para CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Gestión de problemas para exámenes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  problems list --type numeracion --difficulty 3
  problems search "conversión"
  problems stats --detailed
  problems export --format json --output export.json
  problems import --file export.json
  problems delete 12345678 --confirm
  problems backup
  problems restore backups/backup_20260115_120000 --confirm
  problems verify --repair
        """
    )
    
    parser.add_argument('--repo', default='./problems', help='Ruta del repositorio')
    parser.add_argument('--backend', choices=['file', 'sqlite'], default='file', help='Backend')
    
    subparsers = parser.add_subparsers(dest='command', help='Comando')
    
    # COMMAND: list
    list_parser = subparsers.add_parser('list', help='Listar problemas')
    list_parser.add_argument('--type', help='Filtrar por tipo')
    list_parser.add_argument('--difficulty', type=int, help='Filtrar por dificultad')
    list_parser.add_argument('--tag', help='Filtrar por tag')
    list_parser.add_argument('--limit', type=int, default=10, help='Máximo de resultados')
    list_parser.add_argument('--offset', type=int, default=0, help='Saltar N resultados')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Mostrar detalles')
    
    # COMMAND: search
    search_parser = subparsers.add_parser('search', help='Buscar problemas')
    search_parser.add_argument('query', help='Texto a buscar')
    search_parser.add_argument('--limit', type=int, default=10, help='Máximo de resultados')
    search_parser.add_argument('-v', '--verbose', action='store_true', help='Mostrar detalles')
    
    # COMMAND: stats
    stats_parser = subparsers.add_parser('stats', help='Estadísticas')
    stats_parser.add_argument('-d', '--detailed', action='store_true', help='Estadísticas detalladas')
    
    # COMMAND: export
    export_parser = subparsers.add_parser('export', help='Exportar problemas')
    export_parser.add_argument('--output', required=True, help='Archivo de salida')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Formato')
    export_parser.add_argument('--type', help='Filtrar por tipo')
    
    # COMMAND: import
    import_parser = subparsers.add_parser('import', help='Importar problemas')
    import_parser.add_argument('--file', required=True, help='Archivo a importar')
    import_parser.add_argument('--format', choices=['json'], default='json', help='Formato')
    import_parser.add_argument('--skip-duplicates', action='store_true', default=True, help='Saltar duplicados')
    
    # COMMAND: delete
    delete_parser = subparsers.add_parser('delete', help='Eliminar problemas')
    delete_parser.add_argument('id', nargs='?', help='ID del problema a eliminar')
    delete_parser.add_argument('--type', help='Eliminar por tipo')
    delete_parser.add_argument('--difficulty', type=int, help='Eliminar por dificultad')
    delete_parser.add_argument('-c', '--confirm', action='store_true', help='Confirmar sin preguntar')
    
    # COMMAND: backup
    backup_parser = subparsers.add_parser('backup', help='Crear backup')
    backup_parser.add_argument('--output', default='./backups', help='Directorio de backups')
    
    # COMMAND: restore
    restore_parser = subparsers.add_parser('restore', help='Restaurar desde backup')
    restore_parser.add_argument('path', help='Ruta del backup')
    restore_parser.add_argument('-c', '--confirm', action='store_true', help='Confirmar sin preguntar')
    
    # COMMAND: verify
    verify_parser = subparsers.add_parser('verify', help='Verificar integridad')
    verify_parser.add_argument('-r', '--repair', action='store_true', help='Reparar problemas')
    
    args = parser.parse_args()
    
    # Crear CLI
    cli = ProblemsCLI(args.repo, args.backend)
    
    # Ejecutar comando
    if args.command == 'list':
        cli.list(
            type_filter=args.type,
            difficulty=args.difficulty,
            tag=args.tag,
            limit=args.limit,
            offset=args.offset,
            verbose=args.verbose
        )
    elif args.command == 'search':
        cli.search(args.query, limit=args.limit, verbose=args.verbose)
    elif args.command == 'stats':
        cli.stats(detailed=args.detailed)
    elif args.command == 'export':
        cli.export(args.output, format=args.format, type_filter=getattr(args, 'type', None))
    elif args.command == 'import':
        cli.import_from_file(args.file, format=args.format, skip_duplicates=args.skip_duplicates)
    elif args.command == 'delete':
        if args.id:
            cli.delete(args.id, confirm=args.confirm)
        elif args.type or args.difficulty is not None:
            cli.delete_by_filter(args.type, args.difficulty, confirm=args.confirm)
        else:
            print("[ERROR] Especificar ID o filtro (--type, --difficulty)")
    elif args.command == 'backup':
        cli.backup(output_dir=args.output)
    elif args.command == 'restore':
        cli.restore(args.path, confirm=args.confirm)
    elif args.command == 'verify':
        cli.verify(repair=args.repair)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
