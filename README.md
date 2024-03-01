# Generating Unicode from Baraha encoding

This document lists the steps that are followed . The goals of this exercise are as follows
* Generate Unicode PDF documents from the Baraha encoded documents 
   * Taittriya Samhita, Taittriya Aranyaka, Taittriya Brahmana
   * Include the Pada, Samhita , Krama, Jata and Ghana versions of all the documents
* Generate Markdown files from the Baraha encoded documents
   * This is done to facilitate easier editing of the files by multiple people 
* Generate an index of all the Pada terms 

## Summary of the Steps to achieve the same ##

### Step 1 Download the Baraha encoded documents from the VedaVMS website ###

### Step 2 Modify the documents to ensure consistency . These changes are already done ###

### Step 3a Generate the json files for the Samhita Paata ###

### Step 3b Augument the json files with the Pada Paata ###

### Step 3c, 3d, 3e  Augument the json files with Krama, Jata and Ghana versions  ( To be done ) ###

### Step 4 Generate the pdf documents ###

### Step 5 Generate the markdown documents ###

### Step 6 Check-in the files generated as part of Step 2  and Steps 5 into the github repository ###

## Detailed instructions ###

### Step 0 Setup a Python virtual environment ###

  * Ensure Python version is at least 3.9 or more 
  ```
    python3 -mvenv myenv
    source myenv/activate
    pip install requirements.txt
  ```

    
# Install the Adishila Vedic fonts (https://adishila.org)
# Install the texlive package using apt-get install commands
# Install the tool indic_transliteration by following the instructions in
# https://github.com/indic-transliteration/indic_transliteration_py/tree/master

  * This seems to work on Python 3.9 and above . Does not work on Python 3.8
  * Specifically
  * sudo pip install indic_transliteration -U
  * sudo pip install git+https://github.com/indic-transliteration/indic_transliteration_py/@master -U
  *
  * Modify the files after installation 
  # File 1: site-packages/indic_transliteration/sanscript/schemes/roman.py
  * Add the following as Line 27
  ```
   BARAHA = 'baraha'
  ``` 
  # File 2: site-packages/indic_transliteration/sanscript/schemes/data/roman/baraha.toml
  *
  * Remove the lines for symbols 0 - 9 . (Remove 10 lines after Line 73 )

  * Remove the line 115 of "." producing | 
  ```
  "|" = [ ".",]
  ```
  * Add the Alternative (gm) for (gg) as Line 117 
  ```
  "(gg)" = ["(gm)",]
  ```    
  # File 3: site-packages/indic_transliteration/sanscript/__init__.py
  * Add the following line as Line 101  
  ```
   BARAHA = roman.BARAHA  
  ```
### Step 1 Download the Baraha encoded documents from the VedaVMS website ###

```
mkdir inputs
cd inputs
python3 ../fetchBaraha_FromVedaVMS.py > fetch.sh
bash fetch.sh
cd ..
mkdir orig
cd orig
python3 ../fetch.py > fetch.sh
bash fetch.sh
python3 ../doc2txt.py *.docx
```
The files have already been modified and checked in. These changes can be incorporated into the original files also .

There are 9 changes to be done across 7 files . for the Samhita and Pada Paada files. There are many changes in the Aaranyaka files. 
 * TS 1 Baraha.docx
```

1986c1986
< first and last padam ff Seventh praSnam :-
---
> first and last padam of Seventh praSnam :-
```

  * TS 2 Baraha.docx
```
288c288
< aqsmAka#mastuq kEva#laH || (appearing inTS 1.6.12.1)
---
> aqsmAka#mastuq kEva#laH || (appearing in TS 1.6.12.1)
615a616
> 
652a654
> ==================================
```

   * TS 3 Baraha.docx
```
768c768
< ------------------------------------
---
> ---------------------------------------------------------
1007a1008
> ---------------------------------------------------------------
```

  * TS 4 Baraha.docx
```
344c344
< special KOrvai for anuvAkam 29 to 34
---
> special KOrvai for 29-to-34 anuvAkam
1271a1272
> 
```

  * TS 5 Baraha.docx
```
443a444
> TS 5.2.9.5
445d445
< TS 5.2.9.4
448c448
< TS 5.2.9.5
---
> TS 5.2.9.6
453a454
> 
716a718
> 
726c728
< 5.4	 pa~jcamakANDE caturthaH praSnaH - iShTakAtrayABidhAnaM
---
> 5.4	 pa~jcamakANDE caturthaH praSnaH iShTakAtrayABidhAnaM
1723a1726
> 
```
  * TS 1.1 Baraha Pada paatam.docx
```
49,50c49,50
< pyAqyaqdhvaqm | aqGniqyAqH | dEqvaqBAqgamiti# dEva- BAqgam | Urja#svatIH | paya#svatIH | praqjAva#tIqriti# praqjA-vaqtIqH | aqnaqmIqvAH | aqyaqkShmAH | mA | vaqH | stEqnaH | IqSaqtaq | mA | aqGaSa(gm)#saq ityaqGa - Saq(gm)qsaqH | ruqdrasya# | hEqtiH | parIti# | vaqH | vRuqNaqktuq | dhruqvAH | aqsminn | gOpa#tAqvitiq gO -paqtauq | syAqtaq | baqhvIH | yaja#mAnasya | paqSUn | pAqhiq || 1 (43) (A1) 
< (iShE - trica#tvAri(gm)Sat )
---
> pyAqyaqdhvaqm | aqGniqyAqH | dEqvaqBAqgamiti# dEva- BAqgam | Urja#svatIH | paya#svatIH | praqjAva#tIqriti# praqjA-vaqtIqH | aqnaqmIqvAH | aqyaqkShmAH | mA | vaqH | stEqnaH | IqSaqtaq | mA | aqGaSa(gm)#saq ityaqGa - Saq(gm)qsaqH | ruqdrasya# | hEqtiH | parIti# | vaqH | vRuqNaqktuq | dhruqvAH | aqsminn | gOpa#tAqvitiq gO -paqtauq | syAqtaq | baqhvIH | yaja#mAnasya | paqSUn | pAqhiq || 1 (43) 
> (iShE - trica#tvAri(gm)Sat ) (A1)
```
  * TS 1.5 Baraha Pada paatam.docx
```
279a280
> 
```

### Step 3a Generate the json files for the Samhita Paata ###


```
python3 generate_Samhita_json.py inputs/TS\ 1\ Baraha.docx inputs/TS\ 2\ Baraha.docx inputs/TS\ 3\ Baraha.docx inputs/TS\ 4\ Baraha.docx inputs/TS\ 5\ Baraha.docx inputs/TS\ 6\ Baraha.docx inputs/TS\ 7\ Baraha.docx
```
This step generates a file named ***TS.json***
### Step 3b Augument the json files with the Pada Paata ###

```
python3 generate_Pada_json.py inputs/*Pada*.docx
```
This step generates a file named  ***TS_withPada.json*** 

### Step 3c Augument the json files with the Sayana Bhashya ###

```
python3 generate_SayanaBhashya_json.py inputs/KY_Sayana_Kanda1.docx inputs/KY_Sayana_Kanda2.docx inputs/KY_Sayana_Kanda3.docx > x.txt
```
This step generates a file named ***TS_withSayanaBhashya.json***

### Step 3d Augument the json files with the Bhatta Bhaskara Bhashya ###
  
```
python3 generate_BhattaBhashya_json.py inputs/KrshnYjrv_BhattaBhaskaraBhashya.docx >x.txt
```

This step generates a file named ***TS_withBhattaBhashya.json***

### Step 3e Generate the json files with the Taittriya Aaranyaka ###

``` 
python3 generate_TA_json.py inputs/TA\ 1-4\ Baraha.docx inputs/TA\ 5-6\ Baraha.docx inputs/TA\ 7-8\ Baraha.docx >x.txt
```
This step generates a file called ***TA.json*** 


### Step 3f Generate the json files with the Taittriya Brahmanam ###

```
python3 generate_TB_json.py inputs/TB\ 1.1-1.4\ Baraha.docx inputs/TB\ 1.5-1.8\ Baraha.docx inputs/TB\ 2.1-2.4\ Baraha.docx inputs/TB\ 2.5-2.8\ Baraha.docx inputs/TB\ 3.1-3.6\ Baraha.docx inputs/TB\ 3.7-3.12\ Baraha.docx > x.txt
```

This step generates a file called ***TB.json***

### Step 3g Generate the PDF and the markdown files ###

```
python3 generatePDF.py
```

This step generates the files under the ***outputs/pdf*** and ***outputs/md*** directory . There are subdirectories created named _Samhita_ , _Pada_ , _Aaranyaka_ and _Brahmanam_  respectively

Implementation notes

*. The pdflatex engine did not work for multi language files. So I used the polyglassia package of LaTex and that worked only with xelatex

* The latexmk command takes care of generating the pdf again after generating the toc Else the xelatex command had to run twice. 

*. If you want to debug the TeX formatting or look at the aux files replace the tempfile.TemporaryDirectory() with a calls to os.path.dir("temp")
