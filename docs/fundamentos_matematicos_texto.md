# Matemáticas del Procesamiento de Texto y Búsqueda Semántica

Detalle los fundamentos matemáticos y computacionales del procesamiento de texto para tareas de búsqueda semántica.

---

## ¿Qué significa comparar textos?

Dado un conjunto de frases y una consulta, queremos encontrar cuáles frases son "más parecidas" a esa consulta. Esto requiere:

1. Representar frases como objetos matemáticos (vectores, matrices, etc.).
2. Definir una forma de comparar esas representaciones.
3. Optimizar el proceso de búsqueda para ser rápido, incluso con miles o millones de frases.

Entonces es transformar texto libre en vectores numéricos que capturen su significado semántico para realizar comparaciones y búsquedas eficientes.

---

## Preprocesamiento del texto

Antes de comparar frases, se realiza una limpieza para reducir el ruido y homogenizar el contenido:

- **Minúsculas**: "Usuario" → "usuario"
- **Remover puntuación**: "¿Crear usuario?" → "crear usuario"
- **Tokenización**: "crear usuario" → `["crear", "usuario"]`
- **Stopwords**: Eliminar palabras como "el", "la", "de"
- **Lematización o stemming** (opcional): "creando" → "crear"

Esto permite que frases con diferentes formas gramaticales pero igual significado se comparen de forma más precisa.

### Tokenización

Consiste en dividir un texto en unidades llamadas *tokens*, que usualmente son palabras, pero pueden ser subpalabras, caracteres o n-gramas.

Ejemplo:

Texto: `"Crear nuevo usuario"`
Tokens: `["Crear", "nuevo", "usuario"]`

#### Tipos comunes

- **Espaciado**: dividir por espacios
- **Basado en reglas**: eliminar signos de puntuación, acentos
- **Subword (WordPiece, BPE)**: usado en modelos como BERT

### Limpieza y Preprocesamiento

Importancia:

- Reduce ruido e inconsistencias
- Mejora la generalización del modelo

Operaciones típicas:

1. Minúsculas
2. Eliminar puntuación
3. Normalizar palabras (lemmatización, stemming)
4. Quitar palabras vacías (*stopwords*)
5. Expandir contracciones ("it's" → "it is")
6. Separar CamelCase

---

## Representación de texto: Embeddings

Un *embedding* convierte texto en un vector de números reales en $ℝ^n$.

### Definición

Dado un texto $T$, su embedding es:

$\text{Embed}(T) = \vec{v} \in \mathbb{R}^d$

### Propósito

- Palabras/Frases similares tienen vectores cercanos
- Captura el contexto semántico

### Métodos comunes

- Bag of Words (BoW)
- TF-IDF
- Word2Vec / GloVe
- Sentence Transformers (BERT, MiniLM, etc.)

Ejemplo:

- `"crear usuario"` → $\vec{v}_1 \in \mathbb{R}^{384}$
- `"registrar nuevo cliente"` → $\vec{v}_2 \in \mathbb{R}^{384}$

Si son similares, entonces:
$\text{distancia}(\vec{v}_1, \vec{v}_2) \approx 0$

### 1. **BoW (Bag of Words)**

Convertimos una frase en un vector basado en la frecuencia de palabras:

```txt
Frase A: "crear usuario"
Frase B: "eliminar usuario"
```

Vocabulario: `["crear", "eliminar", "usuario"]`

| Frase | crear | eliminar | usuario |
| ----- | ----- | -------- | ------- |
| A     | 1     | 0        | 1       |
| B     | 0     | 1        | 1       |

Cada fila es un vector. Para comparar, usamos una métrica de similitud.


### 2. **TF-IDF (Term Frequency - Inverse Document Frequency)**

Pondera palabras según su frecuencia local y global:

$$
\text{tf-idf}(t, d) = tf(t, d) \cdot \log \left(\frac{N}{df(t)}\right)
$$

- `tf(t, d)`: frecuencia de término `t` en documento `d`
- `df(t)`: número de documentos que contienen el término `t`
- `N`: total de documentos

Esto reduce el peso de palabras comunes y aumenta el de palabras distintivas.

---

## 📏 Comparación entre vectores de texto

### 1. **Distancia Euclidiana (L2)**

$$
\text{dist}(\vec{a}, \vec{b}) = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}
$$

Cuanto menor, más parecidos. Útil para vectores densos.

### 2. **Distancia Coseno (Cosine Similarity)**

$$
\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \cdot \|\vec{b}\|}
$$

Mide el ángulo entre vectores, no su magnitud. Ideal para BoW o TF-IDF:

- 1 → mismos vectores (máxima similitud)
- 0 → ortogonales (sin relación)
- -1 → opuestos (muy raramente usado en NLP)

### Ejemplo

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

texts = ["crear usuario", "eliminar usuario"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
sim = cosine_similarity(X[0:1], X[1:2])
```

---

## ¿Qué son los embeddings?

Los embeddings son vectores densos que representan el significado de una frase. Se entrenan con modelos de aprendizaje profundo (transformers, LSTM, etc.) usando contextos para capturar relaciones semánticas.

- Dimensiones típicas: 384, 512, 768...
- Los modelos modernos (como BERT, MiniLM) generan estos vectores.
- Se pueden comparar con las mismas métricas: L2 o coseno.

> Ejemplo: "crear usuario" y "registrar cuenta" tendrán embeddings cercanos.

---

## 🔍 Búsqueda Semántica

Resumen del proceso:

1. Limpiar y tokenizar el texto.
2. Representar como vector (TF-IDF, BoW, embedding).
3. Comparar con vectores del corpus.
4. Retornar los más similares (según distancia).

Esto es la base matemática, independientemente del modelo o librería que se use. Si bien las herramientas modernas simplifican los pasos, conocer estas bases permite evaluar, adaptar y optimizar mejor los sistemas de búsqueda semántica.
