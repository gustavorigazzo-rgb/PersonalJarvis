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

# pywebview also understands this variable, but PersonalJarvis explicitly passes
# gui="edgechromium" on Windows. Patch start() so the explicit default is replaced
# with Qt without changing the upstream desktop_app implementation.
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
