from .database import create_user, get_users, get_user_by_id
from typing import List, Dict

def create_user_crud(username: str, email: str, password: str) -> Dict:
    return create_user(username, email, password)

def get_users_crud(limit: int = 100, offset: int = 0) -> List[Dict]:
    return get_users(limit, offset)

def get_user_by_id_crud(user_id: int) -> Dict:
    return get_user_by_id(user_id)
