"""
Entry point para CLI de gestión de problemas.

Ejecutar con:
    python -m cli

O usar como módulo:
    from cli import main
    main()
"""

import sys
from cli.problems import main

if __name__ == '__main__':
    sys.exit(main())
