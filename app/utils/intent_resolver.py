from typing import Dict, Set, Optional

class IntentResolver:
    def __init__(self):
        self.intent_groups: Dict[str, Set[str]] = {
            "get": {
                "consultar", "ver", "buscar", "obtener", "recuperar", "listar",
                "mostrar", "leer", "detallar", "verificar", "visualizar", "acceder", "explorar"
            },
            "post": {
                "crear", "registrar", "agregar", "añadir", "insertar", "generar",
                "guardar", "subir", "producir"
            },
            "put": {
                "actualizar", "editar", "modificar", "cambiar", "corregir", "reemplazar", "ajustar"
            },
            "patch": {
                "actualizar", "editar", "modificar", "cambiar", "corregir", "reemplazar", "ajustar"
            },
            "delete": {
                "eliminar", "borrar", "remover", "quitar", "suprimir", "descartar", "limpiar"
            }
        }

    def resolve(self, text: str) -> Optional[Set[str]]:
        """
        Given a text, returns the HTTP method(s) inferred from its intent.
        """
        found = set()
        lower_text = text.lower()
        for method, keywords in self.intent_groups.items():
            if any(keyword in lower_text for keyword in keywords):
                found.add(method)
        return found or None
