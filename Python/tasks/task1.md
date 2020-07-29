### Task 1: Result Display CLI with tests.

#### Create a CLI application to include user information and save it in file.

Input should be through `argparse` rather than `input` or direct `sys.argv` parsing.
I.e.
Choices for subjects: 
    - English
    - Nepali
    - Mathematics or Science
The application will run as:

`python store_result.py --name “name” --dob datestring --score “float/int value” --total “int value”  --subject {choices} --store=FILENAME`

Each consecutive run should append the value if not present or replace when present.
There should be percentage flag while storing which is (score/total)*100.


#### Create a CLI application to display the user result stored above.

The second application will read from --store and display the information.

The display should be readable as if we are viewing the result of someone i.e. date should be human readable etc.

Such as:
`python show_result.py --store=FILENAME`


#### Example:

`python store_result.py --name=Sagar Chalise dob=12/30/1985 --score=50.5 --total=80 --subject=English --store=result.txt`
Should create a “result.txt” file in the same folder where you run the script and have the information stored. You can choose the way you want to store the information.

python show_result.py --store=result.txt

```
Name: Sagar Chalise
DOB: 30 December, 1985
English Score: 50.5
English Total: 80
English Percentage: 63.125
……..
Total Percentage: average of percentage in all subjects
\n ---This is a newline
….Next person data….

OR
Show subjects indented:
English:
    Score:
….
```

**Include test_show_result.py and test_store_result.py as well for your unittests**
