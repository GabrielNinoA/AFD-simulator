# AFD_PyQt6_Simulator.py
# Simulador interactivo de AFD con PyQt6
# Requisitos: pip install PyQt6

import sys
import json
from collections import deque
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QFileDialog,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


def apply_modern_dark_palette(app: QApplication):
  
    BG            = QColor("#0f172a")
    BG_ELEVATED   = QColor("#111827")
    CARD          = QColor("#111827")
    SURFACE       = QColor("#1f2937")
    TEXT          = QColor("#e5e7eb")
    SUBTEXT       = QColor("#cbd5e1")
    DISABLED_TXT  = QColor("#6b7280")
    BORDER        = QColor("#334155")
    HIGHLIGHT     = QColor("#4cc9f0")
    HIGHLIGHT_D   = QColor("#3aa6c8")
    SELECTION_BG  = QColor("#164e63")
    LINK          = QColor("#93c5fd")

    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, BG)
    pal.setColor(QPalette.ColorRole.Base, SURFACE)
    pal.setColor(QPalette.ColorRole.AlternateBase, CARD)
    pal.setColor(QPalette.ColorRole.Button, SURFACE)
    pal.setColor(QPalette.ColorRole.ButtonText, TEXT)
    pal.setColor(QPalette.ColorRole.Text, TEXT)
    pal.setColor(QPalette.ColorRole.BrightText, TEXT)
    pal.setColor(QPalette.ColorRole.WindowText, TEXT)
    pal.setColor(QPalette.ColorRole.ToolTipBase, SURFACE)
    pal.setColor(QPalette.ColorRole.ToolTipText, TEXT)
    pal.setColor(QPalette.ColorRole.PlaceholderText, DISABLED_TXT)
    pal.setColor(QPalette.ColorRole.Highlight, SELECTION_BG)
    pal.setColor(QPalette.ColorRole.HighlightedText, TEXT)
    pal.setColor(QPalette.ColorRole.Link, LINK)
    pal.setColor(QPalette.ColorRole.Dark, BORDER)
    pal.setColor(QPalette.ColorRole.Mid, BORDER)
    pal.setColor(QPalette.ColorRole.Shadow, BORDER)
    app.setPalette(pal)

    app.setStyleSheet(f"""
        QMainWindow, QWidget {{
            background-color: {BG.name()};
            color: {TEXT.name()};
            selection-background-color: {SELECTION_BG.name()};
            selection-color: {TEXT.name()};
            font-size: 14px;
        }}

        QLabel {{
            color: {SUBTEXT.name()};
            font-weight: 500;
            margin-top: 2px;
            margin-bottom: 4px;
        }}

        QLineEdit, QTextEdit, QComboBox, QListWidget, QTableWidget {{
            background-color: {SURFACE.name()};
            color: {TEXT.name()};
            border: 1px solid {BORDER.name()};
            border-radius: 10px;
            padding: 6px 8px;
        }}
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QListWidget:focus, QTableWidget:focus {{
            border: 1px solid {HIGHLIGHT.name()};
            box-shadow: 0 0 0 2px {HIGHLIGHT.name()}33; /* halo sutil */
        }}

        QLineEdit[echoMode="0"]::placeholder {{
            color: {DISABLED_TXT.name()};
        }}

        QPushButton {{
            background-color: {HIGHLIGHT.name()};
            color: #001018;
            border: none;
            border-radius: 10px;
            padding: 8px 12px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {HIGHLIGHT_D.name()};
        }}
        QPushButton:pressed {{
            background-color: {HIGHLIGHT.name()};
            filter: brightness(0.95);
        }}
        QPushButton:disabled {{
            background-color: {BORDER.name()};
            color: {DISABLED_TXT.name()};
        }}

        QComboBox QAbstractItemView {{
            background-color: {SURFACE.name()};
            color: {TEXT.name()};
            border: 1px solid {BORDER.name()};
            selection-background-color: {SELECTION_BG.name()};
            selection-color: {TEXT.name()};
            outline: none;
        }}

        QHeaderView::section {{
            background-color: {BG_ELEVATED.name()};
            color: {SUBTEXT.name()};
            border: none;
            border-bottom: 1px solid {BORDER.name()};
            padding: 8px;
            font-weight: 600;
        }}
        QTableWidget {{
            gridline-color: {BORDER.name()};
            alternate-background-color: {CARD.name()};
        }}
        QTableWidget::item {{
            padding: 6px;
        }}
        QTableWidget::item:selected {{
            background-color: {SELECTION_BG.name()};
            color: {TEXT.name()};
        }}

        QListWidget::item {{
            padding: 6px 8px;
            border-radius: 8px;
        }}
        QListWidget::item:selected {{
            background-color: {SELECTION_BG.name()};
            color: {TEXT.name()};
        }}

        QTextEdit[readOnly="true"] {{
            background-color: {CARD.name()};
        }}

        QScrollBar:vertical, QScrollBar:horizontal {{
            background: transparent;
            border: none;
            margin: 0px;
        }}
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
            background: {BORDER.name()};
            min-height: 24px;
            min-width: 24px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
            background: {HIGHLIGHT.name()};
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
            border: none;
        }}

        QToolTip {{
            background-color: {SURFACE.name()};
            color: {TEXT.name()};
            border: 1px solid {BORDER.name()};
            border-radius: 8px;
            padding: 6px;
        }}
    """)



#        LÓGICA AFD

class AFD:
    def __init__(self, states=None, alphabet=None, initial_state=None, accepting_states=None, transitions=None):
        """
        Representación de un Autómata Finito Determinista (AFD).

        Estructuras:
        - states (Q): conjunto de estados.
        - alphabet (Σ): lista de símbolos válidos (lista para preservar orden de iteración).
        - initial_state (q0): estado inicial.
        - accepting_states (F): conjunto de estados de aceptación.
        - transitions (δ): diccionario anidado con la forma:
              { estado_origen: { simbolo: estado_destino } }
        """
        self.states = set(states or [])
        self.alphabet = list(alphabet or [])
        self.initial_state = initial_state
        self.accepting_states = set(accepting_states or [])
        self.transitions = transitions or {}  # dict: state -> {symbol: next_state}

    def validate(self):
        """
        Verifica la coherencia de la definición del AFD:

        - El estado inicial debe pertenecer a Q.
        - Todos los estados de aceptación deben pertenecer a Q (F ⊆ Q).
        - Cada entrada de δ(s, a) debe:
            * partir de un estado s ∈ Q,
            * usar un símbolo a ∈ Σ,
            * terminar en un estado destino ∈ Q.

        Lanza ValueError si encuentra alguna inconsistencia.
        """
        if self.initial_state and self.initial_state not in self.states:
            raise ValueError("Estado inicial no definido en Q")
        if not self.accepting_states.issubset(self.states):
            raise ValueError("Algunos estados de aceptación no están en Q")
        for s, mapping in self.transitions.items():
            if s not in self.states:
                raise ValueError(f"Transición desde estado inexistente: {s}")
            for sym, dst in mapping.items():
                if sym not in self.alphabet:
                    raise ValueError(f"Símbolo '{sym}' en transiciones no pertenece al alfabeto")
                if dst not in self.states:
                    raise ValueError(f"Estado destino '{dst}' no está en Q")

    def step_by_step(self, input_string):
        """
        Simula el AFD sobre 'input_string' y devuelve:
        - trace: lista de pasos (i, estado_actual, símbolo_leído, estado_siguiente).
                 Si no existe δ(estado_actual, símbolo), el estado_siguiente es None
                 y la simulación se considera rechazada.
        - accepted: bool indicando si el estado final pertenece a F.

        Notas:
        - Primero se valida que todos los símbolos de la cadena estén en Σ.
        - La simulación aplica determinísticamente δ estado a estado.
        """
        # Verificación previa: todos los símbolos deben pertenecer al alfabeto
        for ch in input_string:
            if ch not in self.alphabet:
                raise ValueError(f"Símbolo '{ch}' no pertenece al alfabeto")

        cur = self.initial_state
        trace = []

        for i, ch in enumerate(input_string, start=1):
            # Si falta δ(cur, ch), registramos el fallo y terminamos
            if cur not in self.transitions or ch not in self.transitions[cur]:
                trace.append((i, cur, ch, None))
                return trace, False

            nxt = self.transitions[cur][ch]
            trace.append((i, cur, ch, nxt))
            cur = nxt

        # Aceptación: el estado final debe estar en F
        accepted = cur in self.accepting_states
        return trace, accepted

    def generate_accepted(self, n=10, max_len=20):
        """
        Genera hasta 'n' cadenas aceptadas usando **BFS** (búsqueda en anchura) sobre el
        grafo implícito de configuraciones (estado, cadena).

        Estrategia:
        - Partimos de (q0, "").
        - Por cada nodo, expandimos un paso por cada símbolo del alfabeto (si δ existe).
        - Cuando caemos en un estado de aceptación, registramos la cadena generada.
        - 'max_len' limita la longitud para evitar expansión infinita en lenguajes infinitos.
        - 'visited' evita re-explorar exactamente la misma configuración (estado, cadena).

        Devuelve:
        - Lista con las primeras cadenas aceptadas en orden aproximado de longitud creciente.
        """
        results = []
        queue = deque([(self.initial_state, "")])
        visited = set()

        while queue and len(results) < n:
            state, s = queue.popleft()

            # Evitar reprocesar la misma configuración exacta
            if (state, s) in visited:
                continue
            visited.add((state, s))

            # Registrar cadena si el estado actual es de aceptación
            if state in self.accepting_states and s not in results:
                results.append(s)
                if len(results) >= n:
                    break

            # Límite de longitud para frenar crecimiento
            if len(s) >= max_len:
                continue

            # Expandir vecinos (aplicar δ si está definida)
            for symbol in self.alphabet:
                if state in self.transitions and symbol in self.transitions[state]:
                    queue.append((self.transitions[state][symbol], s + symbol))

        return results

    def to_dict(self):
        """Serializa la definición del AFD a un diccionario listo para JSON."""
        return {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "initial_state": self.initial_state,
            "accepting_states": list(self.accepting_states),
            "transitions": self.transitions
        }

    @staticmethod
    def from_dict(d):
        """Crea un AFD a partir de un diccionario (operación inversa de to_dict)."""
        return AFD(d.get('states', []), d.get('alphabet', []), d.get('initial_state'),
                   d.get('accepting_states', []), d.get('transitions', {}))


EXAMPLES = {
    "Paridad de 1s (par)": {
        "states": ["q0", "q1"],
        "alphabet": ["0", "1"],
        "initial_state": "q0",
        "accepting_states": ["q0"],
        "transitions": {
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q0"}
        }
    },
    "Terminan en 01": {
        "states": ["q0", "q1", "q2"],
        "alphabet": ["0", "1"],
        "initial_state": "q0",
        "accepting_states": ["q2"],
        "transitions": {
            "q0": {"0": "q1", "1": "q0"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q1", "1": "q0"}
        }
    },
    "Solo ceros (0+)": {
        "states": ["q0", "q1"],
        "alphabet": ["0", "1"],
        "initial_state": "q0",
        "accepting_states": ["q0"],
        "transitions": {
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q1"}
        }
    },
    "Binarios con al menos un 1": {
        "states": ["q0", "q1"],
        "alphabet": ["0", "1"],
        "initial_state": "q0",
        "accepting_states": ["q1"],
        "transitions": {
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q1"}
        }
    }
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador AFD - PyQt6")
        self.setMinimumSize(1000, 600)

        self.afd = AFD()

        
        root = QWidget()
        main_layout = QHBoxLayout()
        root.setLayout(main_layout)
        self.setCentralWidget(root)

        left = QVBoxLayout()
        main_layout.addLayout(left, 2)

        left.addWidget(QLabel("Estados (separados por coma):"))
        self.states_input = QLineEdit()
        left.addWidget(self.states_input)

        left.addWidget(QLabel("Alfabeto (símbolos separados por coma):"))
        self.alpha_input = QLineEdit()
        left.addWidget(self.alpha_input)

        left.addWidget(QLabel("Estado inicial:"))
        self.initial_combo = QComboBox()
        left.addWidget(self.initial_combo)

        left.addWidget(QLabel("Estados de aceptación (separados por coma):"))
        self.accept_input = QLineEdit()
        left.addWidget(self.accept_input)

        left.addWidget(QLabel("Transiciones (filas): current_state, symbol, next_state"))
        self.trans_table = QTableWidget(0, 3)
        self.trans_table.setHorizontalHeaderLabels(["Desde", "Símbolo", "Hacia"])
        self.trans_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left.addWidget(self.trans_table)

        trans_btns = QHBoxLayout()
        btn_add_trans = QPushButton("Agregar fila de transición")
        btn_add_trans.clicked.connect(self.add_trans_row)
        trans_btns.addWidget(btn_add_trans)
        btn_del_trans = QPushButton("Eliminar fila seleccionada")
        btn_del_trans.clicked.connect(self.delete_trans_row)
        trans_btns.addWidget(btn_del_trans)
        left.addLayout(trans_btns)

        def_btns = QHBoxLayout()
        btn_load_example = QPushButton("Cargar ejemplo")
        btn_load_example.clicked.connect(self.show_examples_menu)
        def_btns.addWidget(btn_load_example)
        btn_apply = QPushButton("Aplicar definición")
        btn_apply.clicked.connect(self.apply_definition)
        def_btns.addWidget(btn_apply)
        left.addLayout(def_btns)

        file_btns = QHBoxLayout()
        btn_save = QPushButton("Guardar AFD (JSON)")
        btn_save.clicked.connect(self.save_afd)
        file_btns.addWidget(btn_save)
        btn_load = QPushButton("Cargar AFD (JSON)")
        btn_load.clicked.connect(self.load_afd)
        file_btns.addWidget(btn_load)
        left.addLayout(file_btns)

        mid = QVBoxLayout()
        main_layout.addLayout(mid, 2)

        mid.addWidget(QLabel("Evaluar cadena:"))
        eval_row = QHBoxLayout()
        self.input_eval = QLineEdit()
        eval_row.addWidget(self.input_eval)
        btn_eval = QPushButton("Evaluar")
        btn_eval.clicked.connect(self.evaluate_input)
        eval_row.addWidget(btn_eval)
        mid.addLayout(eval_row)

        mid.addWidget(QLabel("Trazado paso a paso:"))
        self.trace_out = QTextEdit()
        self.trace_out.setReadOnly(True)
        mid.addWidget(self.trace_out)

        mid.addWidget(QLabel("Generar primeras 10 cadenas aceptadas:"))
        gen_row = QHBoxLayout()
        btn_gen = QPushButton("Generar")
        btn_gen.clicked.connect(self.generate_strings)
        gen_row.addWidget(btn_gen)
        self.gen_list = QListWidget()
        gen_row.addWidget(self.gen_list)
        mid.addLayout(gen_row)

        right = QVBoxLayout()
        main_layout.addLayout(right, 1)

        right.addWidget(QLabel("Mensajes / Ayuda:"))
        self.info_out = QTextEdit()
        self.info_out.setReadOnly(True)
        right.addWidget(self.info_out)

        right.addWidget(QLabel("Ejemplos incluidos:"))
        self.examples_list = QListWidget()
        for name in EXAMPLES.keys():
            self.examples_list.addItem(name)
        self.examples_list.itemDoubleClicked.connect(self.load_example_from_list)
        right.addWidget(self.examples_list)

        self.info_out.append("Bienvenido al Simulador AFD. Define el autómata a la izquierda y pulsa 'Aplicar definición'.")

   
    def add_trans_row(self):
        r = self.trans_table.rowCount()
        self.trans_table.insertRow(r)

    def delete_trans_row(self):
        r = self.trans_table.currentRow()
        if r >= 0:
            self.trans_table.removeRow(r)

    def show_examples_menu(self):
        items = list(EXAMPLES.keys())
        item, ok = QFileDialog.getOpenFileName(self, "Selecciona un archivo JSON de ejemplo (opcional)")
        if item:
            try:
                with open(item, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.populate_definition_from_dict(data)
                self.info_out.append(f"Cargado ejemplo desde archivo: {item}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar: {e}")
        else:
            QMessageBox.information(self, "Ejemplos", "Puedes cargar un ejemplo doble-click en la lista de la derecha.")

    def load_example_from_list(self, item):
        name = item.text()
        data = EXAMPLES.get(name)
        if data:
            self.populate_definition_from_dict(data)
            self.info_out.append(f"Cargado ejemplo: {name}")

    def populate_definition_from_dict(self, d):
        self.states_input.setText(','.join(d.get('states', [])))
        self.alpha_input.setText(','.join(d.get('alphabet', [])))
        self.accept_input.setText(','.join(d.get('accepting_states', [])))
        self.initial_combo.clear()
        for s in d.get('states', []):
            self.initial_combo.addItem(s)
        if d.get('initial_state'):
            idx = self.initial_combo.findText(d.get('initial_state'))
            if idx >= 0:
                self.initial_combo.setCurrentIndex(idx)

        # Carga de δ desde el diccionario de ejemplo
        self.trans_table.setRowCount(0)
        for src, mapping in d.get('transitions', {}).items():
            for sym, dst in mapping.items():
                r = self.trans_table.rowCount()
                self.trans_table.insertRow(r)
                self.trans_table.setItem(r, 0, QTableWidgetItem(src))
                self.trans_table.setItem(r, 1, QTableWidgetItem(sym))
                self.trans_table.setItem(r, 2, QTableWidgetItem(dst))

    def apply_definition(self):
        """
        Construye un objeto AFD a partir de lo ingresado en la interfaz:
        - Parseo de Q, Σ, q0, F.
        - Construcción de δ leyendo cada fila de la tabla de transiciones.
        - Sincronización del combo del estado inicial.
        - Validación de la definición (puede lanzar errores).
        """
        try:
            # Parseo de entradas de texto -> listas limpias
            states = [s.strip() for s in self.states_input.text().split(',') if s.strip()]
            alphabet = [a.strip() for a in self.alpha_input.text().split(',') if a.strip()]
            initial_state = self.initial_combo.currentText() if self.initial_combo.count() > 0 else None
            accepting_states = [s.strip() for s in self.accept_input.text().split(',') if s.strip()]

            # -------- Construcción de δ (función de transición) --------
            transitions = {}
            for r in range(self.trans_table.rowCount()):
                src_item = self.trans_table.item(r, 0)
                sym_item = self.trans_table.item(r, 1)
                dst_item = self.trans_table.item(r, 2)
                # Ignora filas incompletas
                if not src_item or not sym_item or not dst_item:
                    continue

                src = src_item.text().strip()
                sym = sym_item.text().strip()
                dst = dst_item.text().strip()

                if src not in transitions:
                    transitions[src] = {}
                # Si se repite (src, sym), la última definición prevalece
                transitions[src][sym] = dst
            # -----------------------------------------------------------

            # Actualiza combo del estado inicial con los estados vigentes
            self.initial_combo.clear()
            for s in states:
                self.initial_combo.addItem(s)
            if initial_state and initial_state in states:
                idx = self.initial_combo.findText(initial_state)
                if idx >= 0:
                    self.initial_combo.setCurrentIndex(idx)

            # Construcción y validación del AFD
            self.afd = AFD(states, alphabet, self.initial_combo.currentText(), accepting_states, transitions)
            self.afd.validate()
            self.info_out.append("Definición aplicada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error en la definición", str(e))

    def evaluate_input(self):
        """
        Ejecuta la simulación del AFD para la cadena ingresada y
        muestra un trazado paso a paso. Si falta alguna transición
        durante la ejecución, se informa la razón del rechazo.
        """
        s = self.input_eval.text().strip()
        if not self.afd or not self.afd.states:
            QMessageBox.warning(self, "AFD no definido", "Aplica una definición de AFD antes de evaluar.")
            return
        try:
            trace, accepted = self.afd.step_by_step(s)
            self.trace_out.clear()
            self.trace_out.append(f"Evaluando la cadena: \"{s}\"")
            if not trace and s == "":
                self.trace_out.append("(cadena vacía)")
            for step in trace:
                i, cur, ch, nxt = step
                if nxt is None:
                    # Falta δ(cur, ch): rechazo inmediato con explicación
                    self.trace_out.append(f"{i}. Desde el estado ({cur}) con el símbolo '{ch}' no existe transición -> RECHAZADA")
                    self.trace_out.append("Resultado: RECHAZADA")
                    return
                else:
                    self.trace_out.append(f"{i}. Desde el estado ({cur}) con el símbolo '{ch}' se transita al estado ({nxt}).")
            final_state = trace[-1][3] if trace else self.afd.initial_state
            self.trace_out.append(f"Proceso finalizado. El estado final es ({final_state}).")
            self.trace_out.append(f"Resultado: {'ACEPTADA' if accepted else 'RECHAZADA'}")
        except Exception as e:
            QMessageBox.critical(self, "Error de evaluación", str(e))

    def generate_strings(self):
        """
        Genera y muestra hasta 10 cadenas aceptadas usando el BFS del AFD.
        Si el lenguaje es vacío o el límite de longitud corta la búsqueda,
        se informa en la lista de resultados.
        """
        if not self.afd or not self.afd.states:
            QMessageBox.warning(self, "AFD no definido", "Aplica una definición de AFD antes de generar cadenas.")
            return
        try:
            results = self.afd.generate_accepted(10, max_len=20)
            self.gen_list.clear()
            if not results:
                self.gen_list.addItem("No se encontraron cadenas aceptadas (límite alcanzado o lenguaje vacío).")
            else:
                for r in results:
                    display = r if r != "" else "(cadena vacía)"
                    self.gen_list.addItem(display)
            self.info_out.append(f"Generadas {len(results)} cadenas (máx 10).")
        except Exception as e:
            QMessageBox.critical(self, "Error generación", str(e))

    def save_afd(self):
        if not self.afd or not self.afd.states:
            QMessageBox.warning(self, "AFD no definido", "No hay AFD para guardar.")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Guardar AFD como", filter="JSON Files (*.json)")
        if not fname:
            return
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(self.afd.to_dict(), f, indent=2, ensure_ascii=False)
            self.info_out.append(f"Guardado AFD en: {fname}")
        except Exception as e:
            QMessageBox.critical(self, "Error guardado", str(e))

    def load_afd(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Abrir AFD", filter="JSON Files (*.json)")
        if not fname:
            return
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.populate_definition_from_dict(data)
            # También aplicamos la definición para validar y dejar listo el AFD
            self.apply_definition()
            self.info_out.append(f"Cargado AFD desde: {fname}")
        except Exception as e:
            QMessageBox.critical(self, "Error carga", str(e))


def main():
    app = QApplication(sys.argv)
    apply_modern_dark_palette(app)
    w = MainWindow()
    w.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
