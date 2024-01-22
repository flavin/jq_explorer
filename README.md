# JQ Explorer

JQ Explorer is a Python script that allows you to interactively explore JSON data using the [jq](https://stedolan.github.io/jq/) command-line tool. It provides a command-line interface where you can enter jq commands and see the results highlighted using the Pygments library.


## Installation

To install and run this script, follow these steps:

1. Clone the repository from GitHub:

```
git clone https://github.com/flavin/jqexplorer.git
```

2. Navigate to the project directory:

```
cd jqexplorer
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

Please ensure that you have Python and pip installed on your system before following these steps.

## Usage

To run the script, use the following command:

```
echo '{"name": "John", "age": 30, "city": "New York"}' | python jqexplorer/main.py
```

if you have a file `example.json``
```
{
    "employees": [
        {
            "firstName": "John",
            "lastName": "Doe"
        },
        {
            "firstName": "Anna",
            "lastName": "Smith"
        },
        {
            "firstName": "Peter",
            "lastName": "Jones"
        }
    ]
}
```

then you can

```
cat example.json | python jqexplorer/main.py
```

or

```
curl -s https://pokeapi.co/api/v2/pokemon/  | python3 jqexplorer/main.py
```
![Screenshot using previous json example](images/curl-example.png)


```
head worldcities.csv | python3 jqexplorer/main.py -R -s
Enter jq string: split("\r\n")| [map(sub("\\\"";"";"g")|split(",")) | .[0] as $headers |.[1:][]| with_entries(.key=$headers[.key])]
```
![Screenshot using previous csv](images/csvexample.png)

