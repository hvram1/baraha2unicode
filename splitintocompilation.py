from docx import Document
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import re
import sys
#from doc_utils import escape_for_latex
import jinja2
import subprocess
import tempfile
import os
import json
import urllib.parse
from requests.models import PreparedRequest

outprefix = "outputs/json"
#outpath.mkdir(parents=True, exist_ok=True)
ts_string = Path("TS_withPadaGhanaJataiKrama.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)

output_json_template_string = Path("templates/compiletemplate.json").read_text(encoding="utf-8")
#outputTree = json.loads(template_string)
for kanda in parseTree['TS']['Kanda']:
    kandaInfo=kanda['id']
    for prasna in kanda['Prasna']:
        prasnaInfo=prasna['id']
        for anuvakkam in prasna['Anuvakkam']:
            anuvakkamInfo = anuvakkam['id']
            for panchasat in anuvakkam['Panchasat']:
                outputJson = json.loads(output_json_template_string)
                #print(outputJson)
                panchasatInfo = panchasat['id']
                header=panchasat['header'].strip()
                #print(kandaInfo,prasnaInfo,anuvakkamInfo,panchasatInfo,header)
                kandastr=f"{kandaInfo:03d}"
                prasnastr=f"{prasnaInfo:03d}"
                anuvakkamstr=f"{anuvakkamInfo:03d}"
                panchasatstr=f"{panchasatInfo:03d}.json"
                outpath=Path(f"{outprefix}/{kandastr}/{prasnastr}/{anuvakkamstr}/")
                outputJson["id"]=header
                outputJson["classification"]["kanda"]=kandaInfo
                outputJson["classification"]["prasna"]=prasnaInfo
                outputJson["classification"]["anuvakkam"]=anuvakkamInfo
                outputJson["classification"]["panchasat"]=panchasatInfo
                

                outpath.mkdir(parents=True, exist_ok=True)
                filename = outpath/panchasatstr
                if panchasat.get("SamhitaPaata"):
                    samhita=panchasat['SamhitaPaata'].strip()
                    
                    samhitaLines=re.split("।|॥",samhita)
                    
                        
                    for line in samhitaLines:
                        if len(line)>0:
                            #print(kandaInfo,prasnaInfo,anuvakkamInfo,panchasatInfo,header)
                            outputJson["samhita"]["lines"].append(line.strip())
                            
                if panchasat.get("PadaPaata"):
                    pada=panchasat['PadaPaata'].strip()
                    
                    outputJson["padapaatha"]["lines"].append(pada)
                
                if panchasat.get("KramamPaatha"):
## Krama Paata ##

                    for Vakhyam in panchasat["KramamPaatha"]:
                        v=Vakhyam['Vakhyam']['kramamVakhyam'].strip()
                        outputJson["kramampaatha"]["lines"].append(v)


                if panchasat.get("JataiPaatha"):
## Jatai Paata ##

                    for Vakhyam in panchasat["JataiPaatha"]:
                        v=Vakhyam['Vakhyam']['jataiVakhyam'].strip()
                        outputJson["jataipaatha"]["lines"].append(v)


                if panchasat.get("GhanaPaatha"):
## Ghana Paata ##

                    for Vakhyam in panchasat["GhanaPaatha"]:
                        v=Vakhyam['Vakhyam']['ghanaVakhyam'].strip()
                        outputJson["ghanapaatha"]["lines"].append(v)


                my_json = json.dumps(outputJson,indent=3,ensure_ascii=False, sort_keys=True)
                #print(filename.name)
                with open(filename, "w") as f:
                    f.write(my_json)
