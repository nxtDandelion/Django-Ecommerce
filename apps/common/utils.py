import secrets
import string

from apps.common.models import BaseModel


def generate_unique_code(model: BaseModel, field: str) -> str:
    """
    Function to generate a unique code
    """
    allowed_chars = string.ascii_letters + string.digits
    unique_code = ''.join(secrets.choice(allowed_chars) for _ in range(12))
    similar_object_exist = model.objects.filter(**{field: unique_code}).exists()
    if similar_object_exist:
        return generate_unique_code(model, field)
    return unique_code

def set_dict_attr(obj, data):
    for attr, value in data.items():
        setattr(obj, attr, value)
    return obj