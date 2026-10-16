"""Read author-hosted public archive and compare every numeric input.
Does not overwrite the submitted CSV or infer its original download history.
Run explicitly with internet access: python code/verify_public_source.py
"""
from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import hashlib,json,ssl,sys
import certifi
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
URL='https://davidcard.berkeley.edu/data_sets/njmin.zip'
with urlopen(URL,timeout=60,context=ssl.create_default_context(cafile=certifi.where())) as r: archive=r.read()
with ZipFile(BytesIO(archive)) as z:
    path=ROOT/'data/raw/public.csv'
    columns='SHEET CHAIN CO_OWNED STATE SOUTHJ CENTRALJ NORTHJ PA1 PA2 SHORE NCALLS EMPFT EMPPT NMGRS WAGE_ST INCTIME FIRSTINC BONUS PCTAFF MEALS OPEN HRSOPEN PSODA PFRY PENTREE NREGS NREGS11 TYPE2 STATUS2 DATE2 NCALLS2 EMPFT2 EMPPT2 NMGRS2 WAGE_ST2 INCTIME2 FIRSTIN2 SPECIAL2 MEALS2 OPEN2R HRSOPEN2 PSODA2 PFRY2 PENTREE2 NREGS2 NREGS112'.split()
    if '--create-input' in sys.argv and not path.exists():
        path.parent.mkdir(parents=True,exist_ok=True)
        pd.read_csv(BytesIO(z.read('public.dat')),sep=r'\s+',header=None,names=columns,na_values='.').to_csv(path,index=False)
    if not path.exists(): raise SystemExit('Input missing. Run with --create-input to obtain the public author data.')
    csv=pd.read_csv(path)
    source=pd.read_csv(BytesIO(z.read('public.dat')),sep=r'\s+',header=None,names=csv.columns,na_values='.')
    assert source.shape==csv.shape
    assert np.allclose(source.to_numpy(float),csv.to_numpy(float),equal_nan=True,rtol=0,atol=0)
    for original,local in [('codebook','codebook.txt'),('read.me','author_readme.txt')]:
        (ROOT/'data/raw'/local).write_bytes(z.read(original))
result={'verified_against':URL,'source_archive_sha256':hashlib.sha256(archive).hexdigest(),'csv_sha256':hashlib.sha256((ROOT/'data/raw/public.csv').read_bytes()).hexdigest(),'rows':len(csv),'columns':len(csv.columns),'all_values_and_missingness_identical':True,'note':'Independent verification during review, not evidence of how the initial submission acquired the CSV.'}
(ROOT/'data/source_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('Verified all 410 x 46 input values, including missingness, against author archive.')
