# Sofia Pipeline

This repository contains a Python, cross-Act, pipeline for parsing UK's legislation XML documents, named Sofia.

Sofia was used for producing the results of the following preprint publication:

[1] Graphie: A network-based visual interface for UK's Primary Legislation
    Evan Tzanis, Pierpaolo Vivo, Yanik-Pascal Förster, Luca Gamberi, Alessia Annibale
    https://arxiv.org/abs/2210.02165

The steps of the pipeline are:

- Data Modeling, initialize the declared Graphie Object (file: Sofia Pipeline.ipynb). (Figure 3, section Data Modelling in [1])

- Parser, using native beautifulsoup (https://www.crummy.com/software/BeautifulSoup/) methods parse Housing Act's 2004 full XML content. The parsing is completed in two phases using the following methods contents(url) and singlesection(url).
         contents(url): for each section of the Housing Act 2004, return one section's coresponded UK Legislation URI.  
         singlesection(url): given one section's UK Legislation URI, return a populated memory instance of the Graphie model associated with that section.
        
- Generate the housingact2004.json file. Serialize one section's (last cell in Sofia Pipeline.ipynb ) Graphie Object instance into a JSON file, structured by the following elements (consider section 194):  
      
      * partNumber: "Part 6"
      * partTitle: "Other provisions about housing"
      * chapterNumber: "Chapter 1"
      * chapterTitle: "Secure tenancies"
      * crossHeading: " Suspension of certain rights in connection with anti-social behaviour"
      * section: 
            - Title:
            - Number: 
            - Paragraphs: [
                    - subParagraphs [
                        - Lines
                        ]
                      ]                    
      * subSectionsNum: 4 # total number of included subsections objects
      * paragraphsNum: 10 # total number of included paragraphs objects
      * subParagraphsNum: 0 # total number of included sub paragraphs objects
      * lineNum: 0 ] # total number of single Lines objects
      * ingoing: ["79": 1,"138": 1] # obtained by a repeated application of: refInSingleLine()   
      * outgoing: ["Housing Act 1985": 4, "Housing and Regeneration Act 2008": 1] # obtained by a repeated application of: actsInSingleLine.ipynb
   
   
- Undertake several offline data integrity routines against the housingact2004.json. 
- Transformation service, generate several HTML and JSON files for populating specific front-end components of our web site:
      
      * inbound.json.ipynb: for generating the inbound.json file. 
      * outbound.json.ipynb: for generating the outbound.json file. 
      * divNav().ipynb: Graphie's web navigational links (TOC)
      
- Undertake several offline data integrity routines against the generated components. 

## Primary Data, Input Data 

Each legislation page (either a whole item, or a part, or a section) on legislation.gov.uk, is also offered as an XML file, which we refer to as the XML URL of that page. For instance, the full data of the Housing Act 2004, hosted at https://www.legislation.gov.uk/ukpga/2004/34/, is also available at https://www.legislation.gov.uk/ukpga/2004/34/data.xml

### Output Data

* housingact2004.json: A "flat file" serliazing the full content (about all sections) of the Graphie Object after parsing Housing Act 2004's full XML file. 
* outbound.json: A JSON file populating the network visualization (also including references to external Acts) on . 
* inbound.hson: A JSON file populating the inbound network references between Housing Act's 2004 sections.   

## Other

- This is still work in progress. 
- Sofia is heurisitic in nature. Thus, as pointed above, Sofia's output should be manually checked.





