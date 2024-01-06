from gears import settings


def test_initialized_settings(tmp_path):
    settings_path = tmp_path / "init-settings.toml"
    settings.initialize_settings(settings_path)
    assert settings_path.exists()
    ...
    stg = settings.Settings.load(settings_path)
    assert isinstance(stg, settings.Settings)
