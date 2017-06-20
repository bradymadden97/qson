# QSON
QSON (for Quick JSON) is a JSON-generation tool that allows users to quickly formulate complex data in a ubiquitous structure using simple syntax. Write your data quickly and translate it to JSON format.

**Version 0.1** is a command-line python script that can read in a text file and return a pretty-printed JSON file.
## JSON Generator Syntax
* Key-value pairs are designated with an equals sign ` = `
* The following data types can be represented with the following character conventions:
  * ` s ` for string types (Default)
  * ` i ` for integer types
  * ` f ` for floating-point types
  * ` b ` for boolean types
  * ` [] ` for an array
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

## Usage
**QSON** v0.1 is a Python 3 script.
1. Get [python](https://www.python.org/downloads/)
2. Clone this repository to your machine
3. Run **QSON** with the proper arguments:
`` $ python qson.py <inputfile.txt> <outputfile.json> ``

## Demo
To run a demo of QSON and discover the capabilities, execute with the ` -d ` flag: `` $ python qson.py -d `` .

View the input and output in the `` demo `` subdirectory.



