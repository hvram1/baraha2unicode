# \VAR{ panchasat['header'].strip()} #
\BLOCK{ if panchasat.get("GhanaPaatha") }
\BLOCK{ if prevLink | length >0  }[Prev](\VAR{ prevLink })  \BLOCK{ else } Prev \BLOCK{ endif }
\BLOCK{ if nextLink | length >0  }[Next](\VAR{ nextLink} ) \BLOCK{ else } Next \BLOCK{ endif }
\BLOCK{ for ghana in panchasat['GhanaPaatha']}

# \VAR{ ghana['Vakhyam']['id'].strip() }  _\VAR{ ghana['Vakhyam']['padaVakhyam']}_ #  



\VAR{ ghana['Vakhyam']['reference']} [Raise a correction](\VAR{repository  | my_encodeURL("title",panchasat['header'].strip()+"-"+ghana['Vakhyam']['id'].strip(),"body",ghana['Vakhyam']['padaVakhyam'] + "\n\n\n" + ghana['Vakhyam']['ghanaVakhyam'].strip() ) })

## \VAR{ ghana['Vakhyam']['ghanaVakhyam'].strip() } ##

\BLOCK{endfor}
\BLOCK{ if prevLink | length >0  }[Prev](\VAR{ prevLink })  \BLOCK{ endif }
\BLOCK{ if nextLink | length >0  }[Next](\VAR{ nextLink} )\BLOCK{ endif }
\BLOCK{ endif }
