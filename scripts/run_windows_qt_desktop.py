"""Windows desktop launcher that forces pywebview's Qt backend.

Use this only when the default EdgeChromium/WinForms backend cannot start
(for example when Windows Smart App Control blocks pythonnet's Python.Runtime.dll).

The launcher does not weaken Windows security. It keeps the normal Personal
Jarvis desktop/voice stack, but routes only the embedded UI shell through Qt.
"""

from __future__ import annotations

import os
import sys

if sys.platform != "win32":
    raise SystemExit("This helper is intended for Windows only.")

# Verify the Qt backend first. pywebview normally falls back to WinForms when Qt
# is incomplete; on machines where Smart App Control blocks Python.Runtime.dll,
# that fallback only recreates the original crash. Fail clearly instead.
try:
    import qtpy  # noqa: F401
    from qtpy.QtWebEngineWidgets import QWebEngineView  # noqa: F401
except Exception as exc:
    raise SystemExit(
        "Qt desktop backend is not ready. Run:\n"
        "  python -m pip install \"pywebview[pyside6]\"\n"
        f"Details: {type(exc).__name__}: {exc}"
    ) from exc

os.environ["PYWEBVIEW_GUI"] = "qt"

import webview  # noqa: E402

_original_start = webview.start


def _start_with_qt(*args, **kwargs):
    kwargs["gui"] = "qt"
    return _original_start(*args, **kwargs)


webview.start = _start_with_qt

from jarvis.__main__ import _run_desktop  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(_run_desktop(debug="--debug" in sys.argv))
