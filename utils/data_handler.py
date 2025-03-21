import json
import os
import datetime
from pathlib import Path

# Asegurar que los directorios de datos existan
data_dir = Path("data")
surveys_dir = data_dir / "surveys"
chats_dir = data_dir / "chats"

# Crear directorios si no existen
surveys_dir.mkdir(parents=True, exist_ok=True)
chats_dir.mkdir(parents=True, exist_ok=True)

def save_survey_data(survey_data):
    """
    Guarda los datos de la encuesta en un archivo JSON
    
    Args:
        survey_data (dict): Datos de la encuesta
    """
    # Generar un ID único basado en el nombre y la fecha actual
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in survey_data["name"])
    file_id = f"{safe_name}_{timestamp}"
    
    # Ruta completa del archivo
    file_path = surveys_dir / f"{file_id}.json"
    
    # Guardar como JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(survey_data, f, ensure_ascii=False, indent=4)
    
    return file_id

def save_chat_history(chat_history, file_id=None):
    """
    Guarda el historial de chat en un archivo JSON
    
    Args:
        chat_history (list): Lista de mensajes del chat
        file_id (str, optional): ID del archivo. Si es None, se genera uno nuevo
    """
    if file_id is None:
        # Generar un ID basado en la fecha actual
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = f"chat_{timestamp}"
    
    # Ruta completa del archivo
    file_path = chats_dir / f"{file_id}.json"
    
    # Guardar como JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)
    
    return file_id

def load_chat_history(file_id):
    """
    Carga el historial de chat desde un archivo JSON
    
    Args:
        file_id (str): ID del archivo de chat
        
    Returns:
        list: Historial de chat o lista vacía si no existe
    """
    file_path = chats_dir / f"{file_id}.json"
    
    if not file_path.exists():
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_recent_surveys(limit=10):
    """
    Obtiene las encuestas más recientes
    
    Args:
        limit (int): Número máximo de encuestas a retornar
        
    Returns:
        list: Lista de diccionarios con datos de encuestas
    """
    survey_files = list(surveys_dir.glob("*.json"))
    survey_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    results = []
    for file_path in survey_files[:limit]:
        with open(file_path, "r", encoding="utf-8") as f:
            survey_data = json.load(f)
            results.append({
                "id": file_path.stem,
                "name": survey_data.get("name", "Usuario"),
                "timestamp": datetime.datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "data": survey_data
            })
    
    return results 