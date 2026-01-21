import random
import json
import os
from core.generator_base import ExerciseGenerator
from modules.combinacional.models import KarnaughExerciseData, LogicProblemExerciseData, MSIExerciseData

class KarnaughGenerator(ExerciseGenerator):
    def topic(self) -> str:
        return "Lógica Combinacional"

    def generate(self, difficulty: int = 1) -> KarnaughExerciseData:
        es_minterms = random.choice([True, False])
        target = 1 if es_minterms else 0
        default = 0 if es_minterms else 1
        outputs = [default] * 16

        for _ in range(random.randint(3, 6)):
            idx1 = random.randint(0, 15)
            bit_to_flip = random.randint(0, 3)
            idx2 = idx1 ^ (1 << bit_to_flip)
            outputs[idx1] = target
            outputs[idx2] = target

        return KarnaughExerciseData(
            title="Diseño y Simplificación Lógica",
            description="Dada la función definida por la siguiente tabla de verdad:",
            truth_table_outputs=outputs,
            canon_type="Minitérminos (Suma de Productos)" if es_minterms else "Maxitérminos (Producto de Sumas)",
            gate_type="NAND" if es_minterms else "NOR",
            vars_name=['A', 'B', 'C', 'D'],
            out_name='F'
        )

class LogicProblemGenerator(ExerciseGenerator):
    def __init__(self):
        self.scenarios = self._load_scenarios()

    def _load_scenarios(self):
        path = os.path.join("config", "scenarios.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def topic(self) -> str:
        return "Lógica Combinacional"

    def generate(self, difficulty: int = 1) -> LogicProblemExerciseData:
        if not self.scenarios:
            return LogicProblemExerciseData(
                title="Problema de Diseño Lógico",
                description="Error: No se encontraron escenarios.",
                context_title="Error",
                variables_desc=[],
                output_desc="",
                logic_description="",
                vars_clean=['A','B','C','D'],
                out_clean='Z'
            )

        sc = random.choice(self.scenarios)
        logic = random.choice(sc["logicas"])
        vars_clean = [v.split(':')[0].strip() for v in sc["vars"]]
        out_clean = sc["salida"].split(':')[0].strip()

        return LogicProblemExerciseData(
            title="Problema de Diseño Lógico",
            description="Diseñe el circuito de control para el sistema descrito a continuación.",
            context_title=sc["titulo"],
            variables_desc=sc["vars"],
            output_desc=sc["salida"],
            logic_description=logic,
            vars_clean=vars_clean,
            out_clean=out_clean
        )

class MSIGenerator(ExerciseGenerator):
    def topic(self) -> str:
        return "Sistemas MSI Combinacionales"

    def generate(self, difficulty: int = 1) -> MSIExerciseData:
        tipo = random.choice(['MUX', 'COMPARADOR', 'SUMADOR'])
        params = {}

        if tipo == 'MUX':
            params['inputs'] = [random.randint(0, 1) for _ in range(16)]
            params['cases'] = []
            for _ in range(3):
                params['cases'].append({
                    'addr': random.randint(0, 15),
                    'ena': random.choice([0, 1])
                })
        elif tipo == 'COMPARADOR':
            params['A'] = random.randint(0, 15)
            params['B'] = random.randint(0, 15)
            params['cascada'] = [random.randint(0, 1) for _ in range(3)] # gr, eq, le
        elif tipo == 'SUMADOR':
            params['A'] = random.randint(0, 15)
            params['B'] = random.randint(0, 15)
            params['Cin'] = random.randint(0, 1)

        return MSIExerciseData(
            title="Análisis de Bloques MSI",
            description=f"Dado el siguiente esquema lógico ({tipo}):",
            block_type=tipo,
            params=params
        )
