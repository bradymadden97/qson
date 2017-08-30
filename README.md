# QSON
QSON (for Quick JSON) is a JSON-generation tool that allows users to quickly formulate complex data in a ubiquitous structure using simple syntax. Write your data quickly and translate it to JSON format.

**Version 2.0** includes both a command-line python script that can read in a text file and return a pretty-printed JSON file, and a RESTful webapp that can read in qson input and display pretty-printed JSON.

## JSON Generator Syntax
* Key-value pairs are designated with an equals sign ` = `
* The following data types can be represented with the following character conventions:
  * ` s ` for string types (Default)
  * ` i ` for integer types
  * ` f ` for floating-point types
  * ` b ` for boolean types
  * ` [] ` for an array
  * ` [{index}] ` for an object array
* Nested data is indicated by tabbing-in from the parent on a new line. For example:
```
name s = Brady Madden
age i = 20
address
	street s = 123 Main St.
	city s = Mountain View
 ```
 will generate:
 ```
{  
     "name": "Brady Madden",
     "age": 20,
     "address": {  
          "street": "123 Main St.",
          "city": "Mountain View"
     }
}
 ```
 * Simple arrays can be designated on one line, with comma delimited values, or combined throughout the document:
 ```
 courses[] = math, science
 school = University
 grade i = 12
 courses[] = english
 ```
  to generate:
```
{
     "courses": [
          "math",
          "science",
          "english"
     ],
     "grade": 12,
     "school": "University"
}
```
 * Object arrays can hold multiple objects containing multiple key-value pairs. Objects inside object arrays can be referenced by index:
```
emergencyContacts[0]
    name = John Doe
    phoneNumber = 555-5432
emergencyContacts[1]
    name = Jane Doe
    phoneNumber = 867-5309

emergencyContacts[0]
    relationship = father
```
The object arrays will be combined by index and render:
 ```
"emergencyContacts": [
     {
          "name": "John Doe",
          "phoneNumber": "555-5432",
          "relationship": "father"
     },
     {
          "name": "Jane Doe",
          "phoneNumber": "867-5309"
     },
]
```
 * New objects inside object arrays can also be created by leaving the {index} blank:
```
emergencyContacts[0]
    name = John Doe
    phoneNumber = 555-5432
emergencyContacts[]
    name = Jane Doe
    phoneNumber = 867-5309
emergencyContacts[1]
    relationship = mother
```
 Generates:
 ```
"emergencyContacts": [
     {
          "name": "John Doe",
          "phoneNumber": "555-5432"
     },
     {
          "name": "Jane Doe",
          "phoneNumber": "867-5309",
          "relationship": "mother"
     }
]
```

## Usage
**QSON** v2.0 is both a Python CLI and a RESTful webapp.
### Python CLI
1. Get [python](https://www.python.org/downloads/)
2. Clone this repository to your machine
3. Run **QSON** with the proper arguments:
`` $ python qson.py -i <inputfile.txt>  -o <outputfile.json> ``
### Webapp
1. View and edit **QSON** on the interactive [website](https://qson.herokuapp.com)
2. Edit and download JSON files with one click

## Develop
1. Get [python](https://www.python.org/downloads/) and [node](https://nodejs.org/en/download/)
2. Clone this repository to your machine
3. Run `npm install`

## Demo
To run a demo of QSON and discover the capabilities, execute with the ` -d ` flag: `` $ python qson.py -d `` .

View the input and output in the [demo](qson/demo) subdirectory.



