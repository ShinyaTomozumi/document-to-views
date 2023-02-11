# document_to_views
This program creates a template for a view file from a design document defined.

## How to use
The usage is as follows.

1. Copy the documents under the "_sample" folder.
2. Edit "sample.yaml" or "sample.uif" to create a screen design document.
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
To use this tool on the command line, use the following options.

| Option | Description                                                                                                             |
|--------|-------------------------------------------------------------------------------------------------------------------------|
| -t     | Required.<br>Set the project type.<br/>The following projects are currently supported<br/><br/> - laravel<br/> - nextjs |
| -i     | Required.<br>Specify the path of the document file to be read.                                                          |
| -o     | Optional.<br>Specify the path to which the source code will be written.                                                 |
| -doc   | Optional.<br>Specifies the document type.<br/><br/>Support:<br/> - uiflows<br/> - yaml<br/><br/>Default:<br/> - uiflow  |


## Design document
### - UiFlows file
For more information on "**UiFlows**," see " https://signalvnoise.com/posts/1926-a-shorthand-for-designing-ui-flows ".<br>
Based on this description, create a file including the following specifications<br>
Please check "sample.uif" as a reference document.<br>
Add the following items to the screen description to create the document.<br>
Also, ":" must always appear after "Key".

| Key         | Description                                                                                                                           |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------|
| ID:         | Required.<br>Defines the Id of the screen.<br/>Describe in snake_case.                                                                      |
| TItle:      | Required.<br>Defines the title of the screen.<br/>The name at the time of screen definition is used when you want to display a title. |
| URL:        | Optional.<br>This is required for web-related programs.<br>When defining a path to be passed as a parameter, prefix it with "_".      |
| Desc:       | Optional.<br>Describe the screen description.<br/>This description can have multiple lines.                                           |
| Middleware: | Optional.<br>This will be the middleware used on the screen.<br/>To specify more than one, separate them by commas.                   |
| Query:      | Optional.<br>Used for pages that set parameters in the URL.                                                                           |
| Dialog:     | Optional.<br>Used to display a dialog on the screen.<br>When used, add the following items.<br> - ID:<br> - Desc:                     |


## 
### - Yaml file
Screen design documents are created in yaml.
Please create the following items as described in "sample.yaml".

| Key         | Description                                                                                  |
|-------------|----------------------------------------------------------------------------------------------|
| version     | This is the version that reads yaml.<br/>Currently not in particular use.                    |
| copyright   | The program copyright.<br/>option.                                    　                      |
| author      | Program creator.<br/>option.                                                                 |
| description | This is a description of the document.<br/>required.                                         |
| views       | This is the definition part of the screen.<br/>The screen design is defined below this item. |

The definitions under "views" are shown in the table below.

| Key         | Description                                                                        |
|-------------|------------------------------------------------------------------------------------|
| id(root)    | It will be the ID of the screen.<br/>Naming conventions are defined in snake form. |
| title       | This will be the title of the screen.<br/>required.　                               |
| url         | This is the URL of the screen.<br/>required.                                       |
| description | This is a description of the screen.<br/>required.                                 |
| middleware  | This will be the middleware used on the screen.<br/>Defined by array.<br/>option.  |


## Note
I have experienced first designing the screen and then implementing it in various projects.<br>
However, manually creating the program code from the screen design is difficult enough just to create the file.<br>
Therefore, we developed this tool to save as much time as possible by creating just a template file.<br>
There were many types of documentation available, but we selected those that were easy to manage with Git.<br>
I intend to eventually be able to create it from a simple format, such as Excel.<br>
A screen template is created, and then the programmer simply implements it.<br>
If I can save you any time using this tool, I will be happy.<br>
Thank you!

## Author
* Copyright (c) 2023 Shinya Tomozumi
* Tomozumi System: https://tomozumi-system.com
* Twitter : https://twitter.com/hincoco27