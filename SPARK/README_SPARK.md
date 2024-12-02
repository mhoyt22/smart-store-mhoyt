# smart-sales-spark

This project provides an introduction to using Apache Spark for data processing and analysis. 
It includes hands-on examples for working with Spark DataFrames and instructions for setting up Spark on your local machine.

Apache Spark is a powerful distributed computing framework widely used for big data processing, machine learning, and real-time analytics. 

We can use Spark with structured data using Spark DataFrames, query data with SQL, or process unstructured data using RDDs (Resilient Distributed Datasets).

## Versions Matter!

This guide has been tested with:

-Python 3.10.11 (newest is 3.12.4 - which does NOT work)
-PySpark 3.5.3
-Spark 3.5.3
-JDK 17
-Winutils for Spark 3

## Apache Spark Homepage

Read about Spark’s features and capabilities on the [Apache Spark Homepage](https://spark.apache.org/).

## Apache Spark Examples

Visit the [Apache Spark Examples Page](https://spark.apache.org/examples.html) to work through Spark’s official examples, including:
- DataFrame Example -  demonstrates creating a Spark DataFrame and performing operations like filtering, aggregation, and adding columns.
- SQL Example - illustrates how to query data using Spark SQL.
- RDD Example - ntroduces RDDs for processing unstructured data.
- Streaming Example - shows how to handle real-time data-in-motion with structured streaming.

## Spark Pipeline Project Examples

Explore how different Spark-based projects might be structured by checking the docs folder. 
Each project demonstrates the use of a scalable pipeline architecture tailored to a specific domain.

- [Spark Sales Project](docs/spark-sales.md) - analyzes customer, product, and sales data to generate insights like sales trends and product performance.
- [Spark Social Media Project](docs/spark-social.md) - processes social media data to uncover user engagement patterns, hashtag trends, and sentiment analysis.
- [Spark Internet of Things (IOT) Project](docs/spark-iot.md) - aggregates and visualizes IoT sensor data to detect anomalies, monitor device usage, and analyze trends.
  
## GETTING STARTED
### Set up your machine
Follow the instructions to set up your system first: [Setup for Windows](SETUP_SPARK_WINDOWS.md)
### Activate your local virtual enviroment & install dependencies
1. Update smart sales repository layout (or update scripts to utilize current layout) to match the below. 
2. Follow these steps to manage local enviroment: [Virtual Enviroment](VIRTUAL_ENV.md)
```bash
project/
├── data/prepared
│   ├── customers_data_prepared.csv
│   ├── products_data_prepared.csv
│   ├── sales_data_prepared.csv
├── scripts/
│   ├── step0-pipeline.py           # Orchestrate the pipeline
│   ├── step1-extract.py            # Extract stage: Read data from sources
│   ├── step2-transform.py          # Transform stage: Process data for insights
│   ├── step3-load.py               # Load stage: Save results to storage
│   └── step4-visualize.py          # Visualize results using seaborn or matplotlib
├── notebooks/
│   ├── insights.ipynb             # Notebook orchestrating extract-transform-load (ETL) + visualization
├── .gitignore
├── README.md
└── requirements.txt
```
### Run PySpark Basic Script

1. In VS Code, open a PowerShell terminal in the root project folder. 

2. Activate your local project environment everytime you open a terminal to work on the project. 

```shell
.\.venv\Scripts\activate
```

Protip: After running the command once, you can usually get it back by typing just the initial dot and then hitting the right arrow key  - or use the up arrow to access prior commands. 

1. Execute the script.

```shell
py scripts\step0_pipeline.py
```

Protip: After running the command once, you can usually get it back by typing just the initial py and then hitting the right arrow key - or use the up arrow to access prior commands. 

If you get a Windows Firewall alert regarding the JDK, click Allow. 

### Enhance Functionality
Add or update the files to make your own functionality. 

Paste the contents from the file provided in this repo.

Execute your scripts - or experiment with a Jupyter notebook.

### Troubleshooting
```powershell
$Env:HADOOP_HOME

Test-Path "$Env:HADOOP_HOME\bin\winutils.exe"

$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
```

# BYPASS LOCAL INSTALLATION - TRY IT ON THE WEB

- <https://hub.ovh2.mybinder.org/user/apache-spark-rwmw01td/notebooks/python/docs/source/getting_started/quickstart_df.ipynb>

- <https://colab.research.google.com/drive/1fa2G3YuXx3Isqyby5kFETqmWotFwtqlH?usp=sharing>

- <https://github.com/apache/spark/tree/master/examples/src/main/python>