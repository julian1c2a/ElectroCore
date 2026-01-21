# 🔍 ¿Por Qué Hamming Se Llama "Distancia"?

**Una justificación matemática rigurosa**

---

## La Respuesta Corta

La función de Hamming $d_H(a,b)$ = "número de posiciones donde a y b difieren" **NO es solo un nombre conveniente**.

Es una **verdadera métrica matemática** — lo que significa que satisface los 3 axiomas formales que definen una distancia en matemáticas.

---

## Los 3 Axiomas (Demostración)

### 1️⃣ No-negatividad y Separabilidad

**Enunciado formal:**
$$d_H(a, b) \geq 0 \text{ para todo par } (a,b)$$
$$d_H(a, b) = 0 \iff a = b$$

**Por qué cumple:**

- $d_H$ *cuenta* el número de posiciones donde a[i] ≠ b[i]
- Contar siempre da un número ≥ 0 ✓
- Si a = b, entonces 0 posiciones difieren, luego $d_H = 0$ ✓
- Si a ≠ b, al menos 1 posición difiere, luego $d_H > 0$ ✓

**Ejemplo:**

```
a = 10110
b = 10110  →  d_H(a,b) = 0  (a = b) ✓

a = 10110
b = 10111  →  d_H(a,b) = 1  (a ≠ b) ✓
```

---

### 2️⃣ Simetría

**Enunciado formal:**
$$d_H(a, b) = d_H(b, a)$$

**Por qué cumple:**

- Si la posición i tiene $a[i] \neq b[i]$, entonces también $b[i] \neq a[i]$
- El *conjunto* de posiciones diferentes es idéntico en ambas direcciones
- Por tanto, el *conteo* es el mismo
- Conmutatividad de la comparación ✓

**Ejemplo:**

```
a = 10110
b = 11110

d_H(a,b): posición 2 difiere (1≠1 NO), posición 1 difiere (0≠1 SÍ) → d=1
d_H(b,a): posición 1 difiere (1≠0 SÍ) → d=1

d_H(a,b) = d_H(b,a) = 1 ✓
```

---

### 3️⃣ Desigualdad Triangular

**Enunciado formal:**
$$d_H(a, c) \leq d_H(a, b) + d_H(b, c)$$

**Interpretación**: "El camino directo nunca es más largo que cualquier camino indirecto"

**Demostración Rigurosa:**

Sean $a, b, c$ palabras de un lenguaje $L$ de ancho fijo $n$ sobre un alfabeto $\Sigma$.

Definamos conjuntos de índices donde ocurren diferencias:

- $I_{ab} = \{i : a[i] \neq b[i], \, 0 \leq i < n\}$ (índices donde $a$ y $b$ difieren)
- $I_{bc} = \{i : b[i] \neq c[i], \, 0 \leq i < n\}$ (índices donde $b$ y $c$ difieren)
- $I_{ac} = \{i : a[i] \neq c[i], \, 0 \leq i < n\}$ (índices donde $a$ y $c$ difieren)

Por definición de distancia Hamming:
$$d_H(a,b) = |I_{ab}|, \quad d_H(b,c) = |I_{bc}|, \quad d_H(a,c) = |I_{ac}|$$

**Caso 1: Alfabeto binario** ($\Sigma = \{0,1\}$)

Si $i \in I_{ab} \cap I_{bc}$ (intersección), entonces:

- $a[i] \neq b[i]$ y $b[i] \neq c[i]$

En alfabeto binario, esto implica $a[i] = c[i]$, por lo que $i \notin I_{ac}$.

Por tanto, los índices donde ocurren diferencias en los caminos intermedios $a \to b$ y $b \to c$ que coinciden se "cancelan" en el cálculo directo $a \to c$:

$$d_H(a,c) = |I_{ab} \cup I_{bc}| - |I_{ab} \cap I_{bc}| \leq |I_{ab}| + |I_{bc}| = d_H(a,b) + d_H(b,c)$$

**Caso 2: Alfabeto arbitrario** ($|\Sigma| \geq 2$)

En un alfabeto no necesariamente binario, la situación es más general. Definamos:

- $J = \{i \in I_{ab} \cap I_{bc} : a[i] = c[i]\}$ (índices en la intersección donde $a$ y $c$ coinciden)

El conjunto $J$ contiene exactamente aquellos índices donde:

- $a[i] \neq b[i]$ y $b[i] \neq c[i]$ pero $a[i] = c[i]$

Por definición: $J \subseteq I_{ab} \cap I_{bc}$, luego:
$$|J| \leq |I_{ab} \cap I_{bc}| \leq \min(|I_{ab}|, |I_{bc}|)$$

La distancia $d_H(a,c)$ cuenta solo aquellos índices donde $a[i] \neq c[i]$. En particular:

- Todos los índices en $I_{ab} \setminus I_{bc}$ contribuyen a $d_H(a,c)$
- Todos los índices en $I_{bc} \setminus I_{ab}$ contribuyen a $d_H(a,c)$
- De los índices en $I_{ab} \cap I_{bc}$, solo los que NO están en $J$ contribuyen

Por tanto:
$$d_H(a,c) = |I_{ab} \setminus I_{bc}| + |I_{bc} \setminus I_{ab}| + (|I_{ab} \cap I_{bc}| - |J|)$$
$$= |I_{ab}| + |I_{bc}| - 2|I_{ab} \cap I_{bc}| + |I_{ab} \cap I_{bc}| - |J|$$
$$= |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}| - |J|$$

Dado que $|J| \geq 0$:
$$d_H(a,c) \leq |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}| \leq |I_{ab}| + |I_{bc}|$$

Finalmente:
$$\boxed{d_H(a,c) \leq d_H(a,b) + d_H(b,c)} \, \checkmark$$

**Ejemplo numérico (binario):**

```
a = 10110
b = 10101
c = 11111

I_ab = {2, 4}     (a[2]=1≠0=b[2], a[4]=0≠1=b[4])
I_bc = {0, 2}     (b[0]=1≠1 NO, b[2]=0≠1=c[2], ... Error, recalculando)
       Corrección: b = 10101, c = 11111
       b[0]=1=1, b[1]=0≠1, b[2]=1=1, b[3]=0≠1, b[4]=1=1
       I_bc = {1, 3}
I_ac = {1, 2, 3}  (a[1]=0≠1, a[2]=1≠1 NO... Error)
       a = 10110, c = 11111
       a[0]=1=1, a[1]=0≠1, a[2]=1=1, a[3]=1=1, a[4]=0≠1
       I_ac = {1, 4}

d_H(a,b) = 2, d_H(b,c) = 2, d_H(a,c) = 2
Verificar: 2 ≤ 2 + 2 ✓
```

**Interpretación**: El camino directo de $a$ a $c$ nunca requiere más cambios que pasar por cualquier punto intermedio $b$.

---

## Consecuencias Teóricas

Al satisfacer estos 3 axiomas, la función de Hamming define un **ESPACIO MÉTRICO**.

Esto habilita:

### 1. **Topología Matemática**

- Concepto de "bola abierta": $B_r(p) = \{w : d_H(w, p) < r\}$
- Concepto de "vecindario": ¿Qué códigos están "cerca"?
- Convergencia y límites en secuencias de palabras

### 2. **Análisis Geométrico**

- Tratamos palabras-código como puntos en un espacio
- La distancia Hamming es la métrica natural de ese espacio
- "Distancia mínima" de un código = radio mínimo de la bola más pequeña alrededor de un código

### 3. **Teoría de Códigos Correctores**

- **Capacidad correctora**: Un código con $d_{min} = 2t+1$ puede corregir $t$ errores
- **Capacidad detectora**: Puede detectar $d_{min}-1$ errores
- **Hamming bound**: Cota teórica máxima de eficiencia

### 4. **Algoritmos de Optimización**

- Búsqueda de códigos óptimos usa conceptos de "distancia mínima"
- Programación dinámica y algoritmos greedy se basan en métrica
- Análisis de complejidad depende de propiedades métricas

---

## Comparación: Hamming vs Medidas Ad-Hoc

| Aspecto | Medida Ad-Hoc | Distancia Hamming |
|--------|---------------|------------------|
| ¿Axiomas verificados? | Tal vez, quizás | ✅ SÍ (3/3) |
| ¿Teoría disponible? | Limitada | ✅ Teoría de métricas |
| ¿Garantías matemáticas? | Ninguna | ✅ Propiedades formales |
| ¿Análisis riguroso posible? | Difícil | ✅ Sí |
| ¿Nombre justificado? | "Parecería" | ✅ Probado |

---

## Reflexión Final

**¿Por qué importa que sea una "distancia"?**

Si fuera solo una medida arbitraria (sin cumplir axiomas), tendríamos un número, pero **no la seguridad de que los análisis basados en ese número sean válidos**.

Al ser una verdadera métrica:

- Podemos usar teoremas topológicos
- Podemos confiar en cotas teóricas
- Podemos construir algoritmos con garantías matemáticas
- Podemos justificar por qué un código es "óptimo"

**Eso es lo que significa llamarla "distancia" Hamming de verdad.**

---

## Lectura Adicional

Ver en el código:

- [core/sistemas_numeracion_basicos.py](core/sistemas_numeracion_basicos.py#L1) - Implementación de `distancia_hamming()`
- [tests/test_hamming_lenguaje.py](tests/test_hamming_lenguaje.py) - Tests de las 3 propiedades

Ver en documentación:

- [CONTENIDOS_FE.md § 2.1.1.6.1.8](../CONTENIDOS_FE.md#2.1.1.6) - Teoría completa
- [ROADMAP_Y_CATALOGO.md](ROADMAP_Y_CATALOGO.md#L50) - Justificación ampliada
