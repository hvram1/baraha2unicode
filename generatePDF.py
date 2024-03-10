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

'''
Bug : Need to add the english prefix into the json tree
'''

def my_encodeURL(url,params):
    #x=urllib.parse.quote(URL)
    #print("URL is ",url, "param1 is ",param1,"value1 is ",value1,"param2 is ",param2,"value2 is ",value2)
    #x=urllib.parse.quote(url+"?"+param1+"="+value1+"&"+param2+"="+value2)
    req = PreparedRequest()
    #params = {param1:value1,param2:value2}
    req.prepare_url(url, params)
    #print(req.url)
    return req.url

def CreateGhanaFiles():
    repository="https://github.com/hvram1/baraha2unicode/issues/new"
    outputdir="outputs/md/Ghana"
    textoutputdir="outputs/text/Ghana"
    templateIndexFileName="templates/Ghana_Index.md"
    templateGhanaPaathaFileName="templates/Ghana_main.md"
    templateGhanaPaathaFileNameText="templates/Ghana_main.txt"
    
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%-',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    latex_jinja_env.filters["my_encodeURL"] = my_encodeURL
    ts_string = Path("TS_withPadaGhana.json").read_text(encoding="utf-8")
    parseTree = json.loads(ts_string)
    indexLinks={}
    prevLink=""
    nextLink=""
    prevPanchasat=""
    nextPanchasat=""
    for kanda in parseTree['TS']['Kanda']:
        
        kandaInfo=kanda["id"]
        indexLinks[kandaInfo]=[]
        for prasna in kanda['Prasna']:
            for anuvakkam in prasna['Anuvakkam']:
                for panchasat in anuvakkam['Panchasat']:
                    if panchasat.get("GhanaPaatha"):
                        header=panchasat['header'].strip().replace(" ","_")
                        node = {"nextLink":nextLink,"prevLink":prevLink}
                        kandaInfo=str(kanda["id"])
                        indexLinks[header]=node
                        if len(prevPanchasat)>0:
                            indexLinks[prevPanchasat]["nextLink"]=header+".md"
                            indexLinks[header]["prevLink"]=prevPanchasat+".md"
                        prevPanchasat=header

    for kanda in parseTree['TS']['Kanda']:
        template = latex_jinja_env.get_template(templateIndexFileName)
        kandaInfo=kanda["id"]
        mdFileName=f"{outputdir}/README_Kanda_{kandaInfo}.md"
        #print("Creating file ",mdFileName)
        document = template.render(kanda=kanda)
        with open(mdFileName,"w") as f:
            f.write(document)

        for prasna in kanda['Prasna']:
            for anuvakkam in prasna['Anuvakkam']:
                for panchasat in anuvakkam['Panchasat']:
                    if panchasat.get("GhanaPaatha"):
                        header=panchasat['header'].strip().replace(" ","_")
                        #print("Working with panchasat ",header)
                        template = latex_jinja_env.get_template(templateGhanaPaathaFileName)
                        textTemplate = latex_jinja_env.get_template(templateGhanaPaathaFileNameText)

                        nextLink=indexLinks[header]["nextLink"]
                        prevLink=indexLinks[header]["prevLink"]
                        document=template.render(panchasat=panchasat,repository=repository,nextLink=nextLink,prevLink=prevLink)
                        text_document=textTemplate.render(panchasat=panchasat,repository=repository,nextLink=nextLink,prevLink=prevLink)
                        #panchasatInfo=panchasat['panchasatInfo'].strip()
                        panchasatFile=f"{outputdir}/Kanda-{kandaInfo}/{header}.md"
                        #print("Creating File ",panchasatFile)
                        with open(panchasatFile,"w") as f1:
                            f1.write(document)

                        panchasatTextFile=f"{textoutputdir}/Kanda-{kandaInfo}/{header}.txt"
                        with open(panchasatTextFile,"w") as f1:
                            f1.write(text_document)


def CreateMd (templateFileName,name,DocfamilyName,data):
    outputdir="outputs/md"
    logdir="logs"
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%-',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    #mdFileName=f"{outputdir}/{name}_{DocfamilyName}_Unicode.md"
    
    template = latex_jinja_env.get_template(templateFileName)
    if DocfamilyName == "Samhita":
        outputdir="outputs/md/Samhita"
        mdFileName=f"{outputdir}/{name}_{DocfamilyName}_Unicode.md"
        document = template.render(kanda=data,invocation=invocation,title=title)
    elif DocfamilyName == "Pada":
        outputdir="outputs/md/Pada"
        mdFileName=f"{outputdir}/{name}_{DocfamilyName}_Unicode.md"
        document = template.render(prasna=data,invocation=invocation,title=title)
    elif DocfamilyName == "Aaranyaka":
        outputdir="outputs/md/Aaranyaka"
        mdFileName=f"{outputdir}/{name}_{DocfamilyName}_Unicode.md"
        document = template.render(prapaataka=data,invocation=invocation,title=title)
    elif DocfamilyName == "Brahmanam":
        outputdir="outputs/md/Brahmanam"
        mdFileName=f"{outputdir}/{name}_{DocfamilyName}_Unicode.md"
        document = template.render(prasna=data,invocation=invocation,title=title)
    

    with open(mdFileName,"w") as f:
        f.write(document)

def CreatePdf (templateFileName,name,DocfamilyName,data):
    outputdir="outputs"
    logdir="logs"
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%-',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    TexFileName=f"{name}_{DocfamilyName}_Unicode.tex"
    PdfFileName=f"{name}_{DocfamilyName}_Unicode.pdf"
    TocFileName=f"{name}_{DocfamilyName}_Unicode.toc"
    LogFileName=f"{name}_{DocfamilyName}_Unicode.log"
    template = latex_jinja_env.get_template(templateFileName)
    if DocfamilyName == "Samhita":
        outputdir="outputs/pdf/Samhita"
        document = template.render(kanda=data,invocation=invocation,title=title)
    elif DocfamilyName == "Pada":
        outputdir="outputs/pdf/Pada"
        document = template.render(prasna=data,invocation=invocation,title=title)
    elif DocfamilyName == "Aaranyaka":
        outputdir="outputs/pdf/Aaranyaka"
        document = template.render(prapaataka=data,invocation=invocation,title=title)
    elif DocfamilyName == "Brahmanam":
        outputdir="outputs/pdf/Brahmanam"
        document = template.render(prasna=data,invocation=invocation,title=title)

    tmpdirname="."
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfilename=f"{tmpdirname}/{TexFileName}"

        with open(tmpfilename,"w") as f:
            f.write(document)
        result = subprocess.Popen(["latexmk","-xelatex", "--interaction=nonstopmode","--silent",tmpfilename],cwd=tmpdirname)
        result.wait()
        src_pdf_file=Path(f"{tmpdirname}/{PdfFileName}")
        dst_pdf_file=Path(f"{outputdir}/{PdfFileName}")
        src_log_file=Path(f"{tmpdirname}/{LogFileName}")
        dst_log_file=Path(f"{logdir}/{LogFileName}")
        #src_toc_file=Path(f"{tmpdirname}/{TocFileName}")
        #dst_toc_file=Path(f"{outputdir}/{TocFileName}")
        src_tex_file=Path(f"{tmpdirname}/{TexFileName}")
        dst_tex_file=Path(f"{outputdir}/{TexFileName}")
        
        if result.returncode != 0:
            print('Exit-code not 0  check Code!')
            exit_code=1
        path = Path(src_tex_file)
        if path.is_file():
            src_tex_file.rename(dst_tex_file)  
        path = Path(src_pdf_file)
        if path.is_file():      
            src_pdf_file.rename(dst_pdf_file)
        path = Path(src_log_file)
        if path.is_file():
            src_log_file.rename(dst_log_file)
        #src_toc_file.rename(dst_toc_file)



def escape_for_latex(data):
    if isinstance(data, dict):
        new_data = {}
        for key in data.keys():
            new_data[key] = escape_for_latex(data[key])
        return new_data
    elif isinstance(data, list):
        return [escape_for_latex(item) for item in data]
    elif isinstance(data, str):
        # Adapted from https://stackoverflow.com/q/16259923
        latex_special_chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "\n": "\\newline%\n",
            "-": r"{-}",
            "\xA0": "~",  # Non-breaking space
            "[": r"{[}",
            "]": r"{]}",
        }
        return "".join([latex_special_chars.get(c, c) for c in data])

    return data
ts_string = Path("TS_withPada.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)

DocfamilyName="Samhita"
samhitaTemplateFile=f"templates/{DocfamilyName}_main.tex"
padaTemplateFile="templates/Pada_main.tex"
aaranyakaTemplateFile="templates/Aaranyaka_main.tex"
brahmanamTemplateFile="templates/Brahmanam_main.tex"
ghanamTemplateFile="templates/Ghanam_main.tex"
samhita_md_TemplateFile=f"templates/{DocfamilyName}_main.md"
pada_md_TemplateFile="templates/Pada_main.md"
aaranyaka_md_TemplateFile="templates/Aaranyaka_main.md"
brahmanam_md_TemplateFile="templates/Brahmanam_main.md"



outputdir="outputs"
logdir="logs"
latex_jinja_env = jinja2.Environment(
block_start_string = '\BLOCK{',
block_end_string = '}',
variable_start_string = '\VAR{',
variable_end_string = '}',
comment_start_string = '\#{',
comment_end_string = '}',
line_statement_prefix = '%-',
line_comment_prefix = '%#',
trim_blocks = True,
autoescape = False,
loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

'''#print("running xelatex with ",samhitaTemplateFile)
template = latex_jinja_env.get_template(samhitaTemplateFile)
prasnaInfo=1
prasna=parseTree['TS']['Kanda'][prasnaInfo-1]
for prasna in parseTree['TS']['Kanda']:
    invocation=prasna['Prasna'][0]['invocation'].strip()
    #invocation=invocation.replace("\n","\\\\")
    prasnaInfo=prasna['id']
    title=prasna['title']
    
    for prasna in prasna['Prasna']:
        prasnaInfo=prasna['id']
        CreatePdf(padaTemplateFile,f"TS_{prasnaInfo}_{prasnaInfo}","Pada",prasna)
        CreateMd(pada_md_TemplateFile,f"TS_{prasnaInfo}_{prasnaInfo}","Pada",prasna)
        
    
    CreatePdf(samhitaTemplateFile,f"TS_{prasnaInfo}",DocfamilyName,prasna)
    CreateMd(samhita_md_TemplateFile,f"TS_{prasnaInfo}",DocfamilyName,prasna)

ts_string = Path("TA.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
for prapaataka in parseTree['TA']['Prapaataka']:
    invocation=prapaataka['invocation'].strip()
   
    prapaatakaInfo=prapaataka['id']
    title=prapaataka['title']
    
    CreatePdf(aaranyakaTemplateFile,f"TA_{prapaatakaInfo}","Aaranyaka",prapaataka)
    CreateMd(aaranyaka_md_TemplateFile,f"TA_{prapaatakaInfo}","Aaranyaka",prapaataka)
    

ts_string = Path("TB.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)    
for prasna in parseTree['TB']['Prasna']:
    invocation=prasna['invocation'].strip()
    
    prasnaInfo=prasna['id']
    title=prasna['title']
    
    
    
    
    CreatePdf(brahmanamTemplateFile,f"TB_{prasnaInfo}","Brahmanam",prasna)
    CreateMd(brahmanam_md_TemplateFile,f"TB_{prasnaInfo}","Brahmanam",prasna)
'''
CreateGhanaFiles()

#return exit_code
'''
[Raise a correction](\VAR{ repository}/issues/new?title=\VAR{ panchasat['header'].strip()}-\VAR{ ghana['Vakhyam']['id'].strip() }&body=\VAR{ ghana['Vakhyam']['padaVakhyam']}\\n\\n\VAR{ ghana['Vakhyam']['ghanaVakhyam'].strip() })
'''
