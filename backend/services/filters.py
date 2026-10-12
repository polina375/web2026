from backend.utils.exception import ValidationError
ALLOWED_FILTERS = {
    "fullName",
    "group",
    "isuId",
    "dormNumber",
    "dormitory",
    "room",
    "moveInDate",
    "isForeigner",
}
NUMERIC_FILTERS = {"isuId", "dormNumber", "room"}

def _normalize_key(key):
    return "dormNumber" if key =="dormitory" else key

def _check_allowed(keys):
    for key in keys:
        if key not in ALLOWED_FILTERS:
            raise ValidationError(f"Неизвестный фильтр:{key}")

def _parse_positive_int(key,raw_value):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        raise ValidationError(f"{key} должен быть целым числом")
    if value<=0:
        raise ValidationError(f"{key} должен быть положительным")
    return value

def _parse_bool_string(raw_value):
    if raw_value.lower()=="true":
        return True
    if raw_value.lower()=="false":
        return False
    raise ValidationError("должен быть true или false")

def parse_query_filters(args):
    _check_allowed(args.keys())
    filters = {}
    for key in args:
        value = args.get(key)
        norm_key = _normalize_key(key)
        if norm_key in NUMERIC_FILTERS:
            value = _parse_positive_int(norm_key, value)
        elif norm_key == "isForeigner":
            value = _parse_bool_string(value)
        filters[norm_key] = value
    return filters

def parse_body_filters(data):
    if not isinstance(data, dict):
        raise ValidationError("Фильтры должны быть JSON объектом")
    _check_allowed(data.keys())
    filters = {}
    for key, value in data.items():
        norm_key = _normalize_key(key)
        if norm_key in NUMERIC_FILTERS and not isinstance(value, int):
            raise ValidationError(f"{norm_key} должен быть числом")
        if norm_key == "isForeigner" and not isinstance(value, bool):
            raise ValidationError("isForeigner должен быть true или false")
        filters[norm_key] = value
    return filters
