# \VAR{ title.strip() }    #


_\VAR{invocation.strip()}_


\BLOCK{for prapaataka in prasna['Prapaataka']}

## \VAR{ prapaataka['sectionTitle'].strip()} ##

\BLOCK{ for anuvakkam in prapaataka['Anuvakkam']}
        
## \VAR{ anuvakkam['header'].strip()} ##


\BLOCK{ for panchasat in anuvakkam['Panchasat']}
                  
### TB \VAR{ panchasat['header'].strip()} ###
                  
                  
\VAR{ panchasat['SamhitaPaata'].strip() } _{ \VAR{ panchasat['id']}}_



\BLOCK{endfor}
              
              
\BLOCK{ if anuvakkam.get("SpecialKorvai") }
\BLOCK{ for specialKorvai in anuvakkam['SpecialKorvai']}
## \VAR{ specialKorvai['header'].strip()} ##


\VAR{ specialKorvai['SpecialKorvai'].replace("\n","").strip()}


\BLOCK{endfor}
\BLOCK{ endif }

_\VAR{ anuvakkam['Korvai']}_  ***(A\VAR{ anuvakkam['id']})***


\BLOCK{endfor}

## \VAR{ prapaataka['PrapaatakaKorvai_header'].strip()} ##


\VAR{prapaataka['PrapaatakaKorvai_Sloka'].replace("\n","").strip()}


## \VAR{ prapaataka['Korvai_header'].strip()} ##

\VAR{ prapaataka['Korvai_Sloka'].replace("\n","").strip()}

## \VAR{ prapaataka['firstLastPadams_header'].strip()} ##


\VAR{ prapaataka['firstLastPadams_Sloka'].strip()}

       

## \VAR{ prapaataka['ending'].strip() } ##

        
        
        
\BLOCK{ endfor }

\end{document}

