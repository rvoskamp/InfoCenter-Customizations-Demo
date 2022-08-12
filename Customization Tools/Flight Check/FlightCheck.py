'''
    FlightCheck is a stand-alone module that performs an inspection of customization files.

    Usage:
        Drag and drop the contents of a vendor's customization folder
        
    Output:
        A single log file will be generated in the vendor's folder with the results of the inspection

'''

SupportedFileFormats = ['js','json','py'] # By extensions

SupportedFiles = {
#   File name           List of keywords
    'code.js'       : ['HTTP','HTTPS','COM','.GLOBALS.RESTREQUEST'],
    'sql.py'        : ['IMPORT','CREATE','SELECT','EXECUTE','EXEC','INSERT','UPDATE','DELETE','SET','DROP','TRUNCATE','ALTER'],
    'process.py'    : ['IMPORT'],
    'forms.json'    : ['SCRIPTTRIGGER'],
    'commands.json' : [],
}

BUFFER_SIZE = 8192

import os, sys, hashlib, json, re

args = sys.argv
if len(args) > 1:
    srcFile = args[1]
    path,_,_ = srcFile.rpartition('\\')
    _,_,vendor = path.rpartition('\\')
    logFile = f'{path}\\FlightCheck.log'
    
    with open(logFile,'w', encoding='cp1252') as outputFile:
        LogHeader = """
    FlightCheck
        
    This module has evaluated the contents for the supported files and reported on finding
    certain keywords that may require further investigation.
    
    It will also calculate a SHA1 signature for each file that can be used to lock down a 
    specific version.
    
    At the end it will provide content that can be added to the RESTAPI.JSON file to serve the
    customization to users.
    """
        outputFile.write(f'{"=" * 100}\n{LogHeader}\n{"=" * 100}')
        
        signatures = {}
        ignoredList = []
        ignoredFiles = []
        ignoredFolders = []
        # Cycle through the individual files
        for fileArg in args[1:]:
            _,_,file = fileArg.rpartition('\\')

            if os.path.isfile(fileArg) and file in SupportedFiles.keys():
                name,_,ext = file.rpartition('.')
                try:
                    outputFile.write(f'\n\n\n{fileArg}:')
                    
                    outputFile.write(f'\n\tEvaluating...')
                    wordList = SupportedFiles[file]
                    diagnostics = []
                    lineNum = 0
                    with open(fileArg,'r') as f:
                        while True:
                            lineNum += 1
                            line = f.readline()
                            if not line:
                                break
                            if file == 'code.js':
                                if lineNum == 1 and not line.strip().startswith('ICC.'+vendor):
                                    diagnostics.append(f'{lineNum: >4d}\t{line.strip()}')
                                    diagnostics.append(f'\t\tDoes not have the associated vendor name: {vendor}\n')
                            
                            foundWords = []
                            for eachWord in wordList:
                                # Use word boundaries (\b) to avoid substring matches (ie reCREATEd)
                                matches = re.findall(r'\b%s\b'% eachWord,line,re.IGNORECASE)
                                if matches:
                                    foundWords.append(eachWord)
                            if foundWords:
                                diagnostics.append(f'{lineNum: >4d}\t{line.strip()}')
                                diagnostics.append(f'\t\tContained: {foundWords}\n')
                        f.close()
                        if diagnostics:
                            outputFile.write(f'\n\t\tLine #')
                            for each in diagnostics:
                                outputFile.write(f'\n\t\t{each}')
                    
                    outputFile.write(f'\n\tCalculating...')
                    with open(fileArg,'rb') as f:
                        sha1 = hashlib.sha1()
                        while True:
                            data = f.read(BUFFER_SIZE)
                            if not data:
                                break
                            sha1.update(data)
                        signatures[file] = sha1.hexdigest()
                        f.close()
                    
                    outputFile.write(f'\n\tDone')
                                
                except Exception as e:
                    outputFile.write(f'\nError:')
                    outputFile.write(e)
            else:
                ignoredList.append(file)
            
            
        if ignoredList:
            outputFile.write(f'\n\n{"-" * 100}')
            outputFile.write(f'\n\nThe following have been ignored because they are not supported:\n')
            outputFile.write(f'{json.dumps(ignoredList,sort_keys=True,indent=4)}')
                
        
        LogFooter = """
    "Customizations" : {        <-- (REQUIRED) Configuration for all customizations (contained within)
    
        <vendor> : {            <----- (REQUIRED) Only listed vendors will be sent to the client
        
            "AccessDenied": [   <---------- (Optional) Deny access to users who connect with one
                                            of the listed groups as their primary group.
            ],
            "AccessGranted": [  <---------- (Optional) Grant access to users who connect with one
                                            of the listed groups as their primary group.
            ],
            "Signatures" : {    <---------- (Optional) Lock down specific versions of individual 
                                            to their respective signatures. 
            }
        }
    }
        """
        outputFile.write(f'\n\n{"=" * 100}\n{LogFooter}\n{"=" * 100}\n')
        outputFile.write(f'\nThe following can be used as content for the RESTAPI.JSON (see explantion above):\n\n')
        
        _,_,vendor = path.rpartition('\\')
        output = {
            "Customizations" : {
                vendor : {
                    "AccessDenied": [
                    ],
                    "AccessGranted": [
                    ],
                    "Signatures" : signatures
                }
            }
        }
        outputFile.write(f'{json.dumps(output,sort_keys=True,indent=4)}')
        outputFile.write(f'\n\n{"=" * 100}\n\n')