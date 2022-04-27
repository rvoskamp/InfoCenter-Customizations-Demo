import os, sys, json

args = sys.argv
if len(args) > 1:
    file = args[1]
else: # Default to working directory
    file = os.getcwd()+"\\restapi.json"
print(f'\r\n\tUsing: {file}')

try:
    print(f'\r\n\tLoading...')
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    
    try:
        print("\tSorting...\r\n\tWriting...")
        with open(file,'w', encoding='cp1252') as customFile:
            json.dump(data,customFile,sort_keys=True,indent=4)
        print("\tDone")
        
    except Exception as e:
        print(f'\nError writing:')
        print(e)
    
except Exception as e:
    print(f'\nError loading:')
    print(e)
    pass
    
server = input('\r\n\tHit <Enter> to continue')
    
    