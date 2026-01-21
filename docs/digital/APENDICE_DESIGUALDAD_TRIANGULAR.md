# 📐 APÉNDICE: Demostración Formal de Desigualdad Triangular

**Referencia**: [POR_QUE_DISTANCIA_HAMMING.md](POR_QUE_DISTANCIA_HAMMING.md) - Sección 3️⃣

---

## Notación Formal

Para palabras $a, b, c$ de un lenguaje $L$ sobre alfabeto $\Sigma$ con ancho fijo $n$:

### Conjuntos de Índices

Definimos para todo par de palabras $(x, y)$:

$$I_{xy} = \{i \in \{0,1,\ldots,n-1\} : x[i] \neq y[i]\}$$

Esta es la **representación como conjunto** de los lugares donde $x$ e $y$ difieren.

### Distancia Hamming

Por definición:
$$d_H(x, y) = |I_{xy}|$$

es decir, la **cardinalidad** del conjunto de índices donde difieren.

---

## La Desigualdad Triangular

### Enunciado

Para todo $a, b, c \in L$:
$$d_H(a, c) \leq d_H(a, b) + d_H(b, c)$$

### Demostración Completa

#### Paso 1: Observación fundamental

La clave está en comprender cómo se relacionan los tres conjuntos $I_{ab}$, $I_{bc}$, $I_{ac}$.

**Proposición**: Si $i \notin I_{ab} \cup I_{bc}$, entonces $i \notin I_{ac}$.

**Prueba**:

- Si $i \notin I_{ab}$, entonces $a[i] = b[i]$
- Si $i \notin I_{bc}$, entonces $b[i] = c[i]$
- Por transitividad: $a[i] = c[i]$, luego $i \notin I_{ac}$ ✓

**Contrarrecíproco**: $I_{ac} \subseteq I_{ab} \cup I_{bc}$

Por lo tanto:
$$d_H(a,c) = |I_{ac}| \leq |I_{ab} \cup I_{bc}|$$

#### Paso 2: Aplicar principio de inclusión-exclusión

$$|I_{ab} \cup I_{bc}| = |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}|$$

Por lo tanto:
$$d_H(a,c) \leq |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}|$$

#### Paso 3: Considerar alfabeto binario

Si $|\Sigma| = 2$ (caso binario):

- Si $i \in I_{ab}$, entonces $a[i] \neq b[i]$
- Si además $i \in I_{bc}$, entonces $b[i] \neq c[i]$
- En binario: $a[i] = c[i]$, luego $i \notin I_{ac}$

Esto significa $I_{ab} \cap I_{bc} \cap I_{ac} = \emptyset$ en el caso binario.

Así:
$$d_H(a,c) \leq |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}| \leq |I_{ab}| + |I_{bc}| = d_H(a,b) + d_H(b,c)$$

#### Paso 4: Alfabeto arbitrario

En un alfabeto arbitrario ($|\Sigma| > 2$), los índices en $I_{ab} \cap I_{bc}$ pueden o no estar en $I_{ac}$.

Definamos:
$$J = \{i \in I_{ab} \cap I_{bc} : a[i] = c[i]\}$$

Estos son los índices donde ambas transiciones $a \to b$ y $b \to c$ ocurren, pero el punto de partida $a[i]$ es igual al punto final $c[i]$.

Obviamente: $J \subseteq I_{ab} \cap I_{bc}$, por lo que $|J| \leq |I_{ab} \cap I_{bc}|$.

Los índices que contribuyen a $d_H(a,c)$ son precisamente:

- Todos en $I_{ab} \setminus I_{bc}$ (contribuye 1 a d_H(a,b), 0 a d_H(b,c), 1 a d_H(a,c))
- Todos en $I_{bc} \setminus I_{ab}$ (contribuye 0 a d_H(a,b), 1 a d_H(b,c), 1 a d_H(a,c))
- Los de $I_{ab} \cap I_{bc}$ excepto $J$ (contribuyen 1+1 a lado derecho, 1 a lado izquierdo)

Por tanto:
$$d_H(a,c) = |I_{ab} \setminus I_{bc}| + |I_{bc} \setminus I_{ab}| + |I_{ab} \cap I_{bc}| - |J|$$

Usando $|A \setminus B| = |A| - |A \cap B|$:
$$d_H(a,c) = (|I_{ab}| - |I_{ab} \cap I_{bc}|) + (|I_{bc}| - |I_{ab} \cap I_{bc}|) + |I_{ab} \cap I_{bc}| - |J|$$
$$= |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}| - |J|$$

Como $|J| \geq 0$:
$$d_H(a,c) \leq |I_{ab}| + |I_{bc}| - |I_{ab} \cap I_{bc}| \leq |I_{ab}| + |I_{bc}|$$

Finalmente:
$$\boxed{d_H(a,c) \leq d_H(a,b) + d_H(b,c)} \quad \checkmark$$

---

## Interpretación Geométrica

La desigualdad triangular dice que en el "espacio de palabras-código" con métrica $d_H$:

- No hay "atajos": el camino directo de $a$ a $c$ nunca es más largo que pasar por un punto intermedio $b$
- Los tres puntos $a, b, c$ forman un triángulo en este espacio métrico
- La distancia directa es la más corta posible (propiedad de métrica)

### Corolario: Propiedad de Minimalidad

Para cualquier camino de $n$ pasos:
$$d_H(a, c) \leq d_H(a, w_1) + d_H(w_1, w_2) + \cdots + d_H(w_{n-1}, c)$$

El camino directo es siempre óptimo (esto se llama **métrica** en análisis).

---

## Ejemplos Concretos

### Ejemplo 1: Binario, 5 bits

```
a = 11010
b = 10011
c = 00011

Comparaciones:
a[0]: 1=1, b[0]: 1≠0, c[0] → a≠b, b≠c, a≠c
a[1]: 1=1, b[1]: 0≠0 NO → a=b
a[2]: 0=0, b[2]: 0=0 → a=b, b=c, a=c
a[3]: 1=1, b[3]: 1=1 → a=b, b=c, a=c
a[4]: 0=0, b[4]: 1=1 → a=b, pero b≠c, a=c

I_ab = {0, 4}  (posiciones 0 y 4)
I_bc = {0}     (posición 0)
I_ac = {0, 4}  (posiciones 0 y 4)

d_H(a,b) = 2
d_H(b,c) = 1
d_H(a,c) = 2

Verificar: 2 ≤ 2 + 1 = 3 ✓
```

Nota: aquí $I_{ab} \cap I_{bc} = \{0\}$, y en esa posición $a[0] = c[0] = 1$, luego $0 \in J$.

### Ejemplo 2: Alfabeto ternario, 3 posiciones

```
a = 012  (posición 0: '0', posición 1: '1', posición 2: '2')
b = 121  (posición 0: '1', posición 1: '2', posición 2: '1')
c = 210  (posición 0: '2', posición 1: '1', posición 2: '0')

Comparaciones:
a[0]=0, b[0]=1, c[0]=2: a≠b, b≠c, a≠c
a[1]=1, b[1]=2, c[1]=1: a≠b, b≠c, a=c
a[2]=2, b[2]=1, c[2]=0: a≠b, b≠c, a≠c

I_ab = {0, 1, 2}  (todas las posiciones)
I_bc = {0, 1, 2}  (todas las posiciones)
I_ac = {0, 2}     (posiciones 0 y 2)

d_H(a,b) = 3
d_H(b,c) = 3
d_H(a,c) = 2

J = {1}  (posición donde a≠b, b≠c, pero a=c)

Verificación algebraica:
d_H(a,c) = |I_ab| + |I_bc| - |I_ab ∩ I_bc| - |J|
         = 3 + 3 - 3 - 1 = 2 ✓

Verificar desigualdad: 2 ≤ 3 + 3 = 6 ✓
```

---

## Conclusión

La desigualdad triangular es **rigorosa y general**:

- ✓ Válida para alfabetos binarios y arbitrarios
- ✓ Depende de estructura de conjuntos de índices
- ✓ El conjunto $J$ captura la "cancelación" de cambios
- ✓ Garantiza que $d_H$ define un espacio métrico

Por tanto, la **Distancia Hamming es matemáticamente rigurosa como métrica**.
