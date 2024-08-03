def phone2wid(*, phone: str) -> str:
    """ TODO: Verificar si todos los `wid` terminan en @c.us"""
    return f"{phone.lstrip('+')}@c.us"
