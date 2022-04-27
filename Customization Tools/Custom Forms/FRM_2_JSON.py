import sys
import json

# Currently supported custom fields
SupportedBlockTranslations =  ['form','buffer','edit','checkbox','push','box','text','radiogroup','list','line']

def TranslateBlock(formBlock,clientWidth):
	status = 'ok'
	data = {}
	blockLines = formBlock.split('\n')
	
	data['fldtype'] = blockLines[0].split(']')[0].lower() # xxxx in [CMSxxxx] is the type, where '[CMS' has already been removed

	if data['fldtype'] not in SupportedBlockTranslations:
		status = 'Unsupported'
	else: # Process remaining lines in the block
		for eachLine in blockLines[1:]:
			line = eachLine.strip()
			if line and '=' in line:
				key, value = line.split('=', 1)

				if key == "clientWidth":
					if data['fldtype'] == 'form':
						clientWidth = int(value)
				
				# Update (1:1) known field data
				elif key in ['Name','Type','KeyType','DataType','MaxChars','Value','Lookup','Table','Filter','CheckedTrigger','UncheckedTrigger','Format','MVInfo','Validation']:
					data[key.lower()] = value
				
				# Translate known key values and update known field
				elif key == "Info":
					x, y, width, height, flags = value.split(',')
					data["x"] = int(x)
					data["y"] = int(y)
					if width != '0':
						data["w"] = int(width)
					if height != '0':
						data["h"] = int(height)
					flags = int(flags, 16)
					if data['fldtype'] == 'edit': 
						if data["x"] > clientWidth:
							flags |= FIELD_HIDDEN
					data["flags"] = flags

				elif key == 'SQLInfo':
					if data['fldtype'] != 'list':
						data[key.lower()] = value

				elif key == "Prompt":
					amp = value.find('&')
					if amp != -1: # Remove '&' hot key
						value = value[:amp] + value[amp+1:]
					data[key.lower()] = value

				elif key == "Buttons":
					amp = value.find('&')
					while amp != -1:
						value = value[:amp] + value[amp+1:]
						amp = value.find('&')
					if "buttons" in data:
						data["buttons"] += '|' + value
					else:
						data[key.lower()] = value

				elif key.startswith("Column"):
					tokens = value.split(',')
					if data['fldtype'] == 'edit':
						if len(tokens)>=5:
							choices = tokens[5].split(';')
							if "selections" not in data:
								data["selections"] = []
							for choice in choices:
								if choice and choice[:2] == '[=':
									rsb = choice.find(']')
									choice = choice[rsb+1:]
									data["selections"].append({"display":choice})
					elif data['fldtype'] == 'list':
						data[key.lower()] = value
						if "cols" not in data:
							data["cols"] = []
						x = int(tokens[1])
						y = int(tokens[2])
						data["cols"].append({"prompt":tokens[0],"x":x,"y":y})

				elif key.startswith("Row"):
					if 'selections' in data:
						row = int(key[3:])
						if row < len(data['selections']):
							data["selections"][row]["value"] = value

				elif key.startswith("SQLCol"):
					if data['fldtype'] == 'list':
						data[key.lower()] = value
			elif line and 'RadioGroup' in blockLines[0] and key == "Buttons":
				value = line.replace('\r', '')
				if "buttons" in data:
					data["buttons"] += '|' + value
				else:
					data[key.lower()] = value

	if data['fldtype'] == 'checkbox':
		# Initialize check box attributes that do not appear in the definition
		if not data.get('value'): # Default for missing value '0' and '1/0' triggers
			data['value'] = '0'
			data['checkedtrigger'] = '1'
			data['uncheckedtrigger'] = '0'
		else: # Defaults for missing triggers are either '1/0' or 'Y/N'
			if not data.get('checkedtrigger'):
				data['checkedtrigger'] = '1' if data['value'].isdigit() else 'Y'
			if not data.get('uncheckedtrigger'):
				data['uncheckedtrigger'] = '0' if data['value'].isdigit() else 'N'
        
	return status,data
    
args = sys.argv
if len(args) > 1:
    frmFile = args[1]
    name,_,ext = frmFile.rpartition('.')
    jsonFile = f'{name}.JSON'
    logFile = f'{name}.log'
    clientWidth = 1000 # Default
    
    with open(logFile,'w', encoding='cp1252') as outputFile:
        
        outputFile.write(f'Using: {frmFile}')

        try:
            outputFile.write(f'\nLoading...')
            with open(frmFile, encoding='utf-8') as f:
                data = f.read()
            
            try:
                
                formDef = { # Form definition
                    "data" :{
                        "localonly": True,  # Do not send to DM Server
                        "defs" : []         # Field definitions in tab order
                    }
                }
                jsonBlocks = []

                outputFile.write("\nParsing...")
                # Blocks start with [CMSxxxx] and appear in tab order
                formBlocks = data.split('[CMS')
                
                outputFile.write("\nProcessing...")
                displayHeader = True
                for eachBlock in formBlocks:
                    status,dataOut = TranslateBlock(eachBlock,clientWidth)
                    if status == 'ok':
                        jsonBlocks.append(dataOut)
                    elif eachBlock: # Ignore blank lines
                        if displayHeader:
                            outputFile.write("\n\nOmitting unsupported fields:\n\n")
                            displayHeader = False
                        outputFile.write(f'[CMS{eachBlock}')
       
                for eachBlock in jsonBlocks:
                    if eachBlock['fldtype'] == 'form':
                        for formKey in eachBlock:
                            formDef['data'][formKey] = eachBlock[formKey]
                    else:
                        fieldDef = {}
                        for fieldKey in eachBlock:
                            fieldDef[fieldKey] = eachBlock[fieldKey]
                        # Insert place holder definitions
                        if eachBlock['fldtype'] == 'box':
                            fieldDef["fields"] = ["--- Replace with field definitions ---"]
                        elif eachBlock['fldtype'] == 'push':
                            fieldDef["scripttrigger"] = { "script": "--- Replace with script name (as defined in code.js) ---" }
                        formDef['data']['defs'].append(fieldDef)

                outputFile.write("\nWriting...")
                with open(jsonFile,'w', encoding='cp1252') as customFile:
                    customFile.write(json.dumps(formDef,indent=4))

                outputFile.write(f'\nCreated: {jsonFile}')
                
            except Exception as e:
                outputFile.write(f'\nError writing:')
                outputFile.write(e)
                pass
        
        except Exception as e:
            outputFile.write(f'\nError loading:')
            outputFile.write(e)
            pass
   
