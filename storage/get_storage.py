from storage.local import LocalStorage
from storage.protocols import Storage


def get_storage() -> Storage:
    return LocalStorage()
