# -*- coding: utf-8 -*-
import runpy
from pathlib import Path

if __name__ == "__main__":
    gui_pyw = Path(__file__).resolve().parent / "gui.pyw"
    runpy.run_path(str(gui_pyw), run_name="__main__")
