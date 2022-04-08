# InfoCenter Customizations
## Overview
InfoCenter supports **multiple** customizations by using a simple folder structure.

Each folder within the *custom* folder will be presented to the client as a self-contained customization. The client will then retrieve the required resources from each folder and incorporate them, giving them a consistent look and feel.

Since each folder can support one or many customizations, you should provide a name that helps identify its content.

**IMPORTANT** The name must not contain any of these reserved characters: `Space` , `Comma` , `Slash` , `Period`

## Getting started
InfoCenter allows customizations at both the client and REST API sides. To take full advantage of this capability you should become familiar with JavaScript, JSON and Python.



### Contents
We provide a template to help with the initial experience. The contents will demonstrate what is currently available and serve as starting point for your future development.

**Note:** Internally, the folder name is referred to as *vendor*

**Files:**

**sql.py** is a file is used to enable *vendor* access to custom SQL REST API module. Each additional *vendor* must be added manually to [sql.py](./sql.py) before it will work and will require a restart of the REST API
```
    if vendor == "demo": #   Simple examples to show what is available
        from edocs.custom.demo.sql import GetCustomSQL
#    elif vendor == "<FolderName>": #   Example for how to add another vendor
#        from edocs.custom.<FolderName>.sql import GetCustomSQL
    else:
        return "Not implemented",""
```


**process.py** is a file is used to enable *vendor* access to custom Process REST API module. Each additional *vendor* must be added manually to [process.py](./process.py) before it will work and will require a restart of the REST API
```
    if vendor == "demo": #   Simple examples to show what is available
        from edocs.custom.demo.process import GetCustomProcess
#    elif vendor == "<FolderName>": #   Example for how to add another vendor
#        from edocs.custom.<FolderName>.process import GetCustomProcess
    else:
        return "Not implemented",""
```

**Folders:**

**demo** is a folder that contains self-contained customizations

See details about the contents of the *demo* folder [here](./demo/)