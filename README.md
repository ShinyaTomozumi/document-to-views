# document_to_views
This program creates a template for a view file from a design document defined in yaml.

## How to use
The usage is as follows

1. Copy "sample.yaml".
2. Edit "sample.yaml" to create a screen design document.
3. Copy "sample_run.sh" and set options as needed.<br/>Options are listed below.
4. Run the edited "sample_run.sh".

## Requirement
The environment in which this program operates is as follows.<br/>
It is possible that it will work even if the version is small.<br/>
But no guarantees.<br/>

 - python v3.9

Install the library with the following command to read the YAML file.
```commandline
pip install pyyaml
```

## Options

| Option | Description                                                                                   |
|--------|-----------------------------------------------------------------------------------------------|
| -t     | Required.<br>Set the project type.<br/>The following projects are currently supported<br/><br/> - laravel  |
| -i     | Required.<br>Specify the path of the yaml file to be read.                                                 |
| -o     | Optional.<br>Specify the path to which the source code will be written.                                                 |

## Design document (Yaml file)
Screen design documents are created in yaml.
Please create the following items as described in "sample.yaml".

| Key         | Description                                                               |
|-------------|---------------------------------------------------------------------------|
| version     | This is the version that reads yaml.<br/>Currently not in particular use. |
| copyright   | The program copyright.<br/>option.                                        |
| author      | Program creator.<br/>option.                                              |
| description | This is a description of the document.<br/>required.                      |
| views       | This is the definition part of the screen.<br/>The screen design is defined below this item.                                    |

The definitions under "views" are shown in the table below.

| Key         | Description                                                   |
|-------------|---------------------------------------------------------------|
| id(root)    | It will be the ID of the screen.<br/>Naming conventions are defined in snake form. |
| title       | This will be the title of the screen.<br/>required.                                   |
| url         | This is the URL of the screen.<br/>required.                                    |
| description | This is a description of the screen.<br/>required.                                     |
| middleware  | This will be the middleware used on the screen.<br/>Defined by array.<br/>option.             |

## Note
I use time and effort to create multiple screen files for various projects.<br>
Therefore, we created this program, which is designed in a document and created in a batch.<br>
For the design documents, the reason we chose yaml was that we needed something that could be managed in text format.<br>
If the design documents are in Excel, it will be difficult to manage them in Git.<br>
If the design document is in csv, it will be difficult to break lines to explain.<br>
So we decided to create a design document in yaml.<br>
If you know of any other good document management methods, please let me know.<br>
Thank you!


## Author
 
* Shinya Tomozumi
* Hinco System
* Twitter : https://twitter.com/hincoco27