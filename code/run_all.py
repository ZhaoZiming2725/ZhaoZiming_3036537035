"""Run from any working directory: python code/run_all.py."""
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for script in ['analysis.py','build_report.py']:
    subprocess.run([sys.executable,str(HERE/script)],check=True)
print('Validated tables, figures, report.html and report.pdf regenerated.')
