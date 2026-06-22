# Laboratorio: Minimax y Poda Alfa-Beta

## Descripción
Este proyecto implementa los algoritmos Minimax y Poda Alfa-Beta para resolver un árbol de decisión simplificado.

## Objetivo
Comparar el resultado y la eficiencia de Minimax frente a Poda Alfa-Beta.

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
```bash
python -m src.main
```

## Pruebas
```bash
pytest --cov=src --cov-report=term-missing

## Tic Tac Toe
```bash
python -m src.tic_tac_toe