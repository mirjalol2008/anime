import uuid

def generate_link_id():
    return str(uuid.uuid4())[:8]