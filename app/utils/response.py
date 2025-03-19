from flask import jsonify
from typing import Dict, Any, Tuple


def create_response(data: Dict[str, Any], status_code: int = 200) -> Tuple:
    return jsonify(data), status_code
