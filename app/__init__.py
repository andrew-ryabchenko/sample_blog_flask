"""Initialize the app."""
import importlib

def make_app(name: str = None, login_disabled: bool = False):
    """Provides optional additional configurations to the app.
    Mainly used during testing."""

    from app import app
    #Re-importing app module to make the Flask app state reset
    #when using this factory function second time
    #in the single interpreter session.
    importlib.reload(app)

    if name:
        app.app.config["application_name"] = name
    if login_disabled:
        app.app.config["LOGIN_DISABLED"] = True

    return app.app