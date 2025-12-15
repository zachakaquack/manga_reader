from settings.settings import Settings

_SETTINGS: Settings | None = None

def load_settings() -> Settings:
    global _SETTINGS
    if _SETTINGS is None:
        # TODO:
        # implement reading from a file

        _SETTINGS = Settings()

    return _SETTINGS
