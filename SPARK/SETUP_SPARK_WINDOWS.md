# Setting Up Spark on Windows

This guide explains how to set up Apache Spark on a Windows system.

We use PySpark and Python to interact with the Spark processing engine. 

Note: At the time of this guide, Spark runs on Java 8/11/17. We will install JDK 17. 

Note: In this guide we are working in your Windows environment, not VS Code. 
**After** completing this work, we suggest you **restart your computer** to finalize configuration. 

-----

## Versions Matter!

This guide has been tested with:

-Python 3.12.4
-PySpark 3.5.3
-Spark 3.5.3
-JDK 17
-Winutils for Spark 3

## Download and Install Python 3.10.11

Ensure Python 3.10.11 is installed and available. 

1. Download [Windows installer (64-bit)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe) to your Downloads folder. Click or double-click to run the exe.

![Windows Python Add to Path](Windows_Python_Add_to_Path.png)

Verify it installs - for just the user, it will go in (change yourname to your user name)

C:\Users\yourname\AppData\Local\Programs\Python

For all users, it might go in: C:\Program Files\Python310\


## Install Java Development Kit (JDK)
  
1. Download and install JDK 11 or 17 from [Adoptium](https://adoptium.net/) for an open-source JDK.

2. Scroll down, click "Other platforms and versions"

3. Use the dropdowns to limit the options. We want Windows / Any / JDK / 17 - LTS.

![Windows JDK](Windows_JDK_17.png)

Click on the JDK .msi file and download to your Downloads folder.

When download is complete, click or double-click on the .msi file to run it. 

Install for ALL users of this machine. 

Java 17 must be added to your system environment variable named Path. 
We do this later. 

## Install Apache Spark  

1. Go to your Documents folder and create a folder named spark. 

2. Download Apache Spark from the [Spark website](https://spark.apache.org/downloads.html). 

3. Save the .tgz file to your new  Documents\spark folder. 

4. Extract the file. Right click on the tgz file / Extract all. 

Extraction may nest folders (e.g., spark-3.5.3-bin-hadoop3/spark-3.5.3-bin-hadoop3). You can adjust or leave the path as is. 

Spark must be added to your system environment variable named Path. 
We do this later.

## Install Hadoop Winutils

1. Go to your Documents folder and create a folder named hadoop. 

2. Make a subfolder in hadoop named bin.
   
3. Download [winutils.exe](https://github.com/steveloughran/winutils/blob/master/hadoop-3.0.0/bin/winutils.exe) from [WinUtils GitHub](https://github.com/steveloughran/winutils).  

4. Place winutils.exe in your Documents/hadoop/bin folder. 

Hadoop must be added to your system environment variable named Path. 
We do this later.

## Edit System Environment Variables

Hit the Windows key. Start typing edit system environment variables. 
Select the option when it appears. 

Click "Environment Variables" button at the bottom.

See "System variables" in the lower half of the screen. 

### Add New Variables

Click New to create a new variable. 
We will need the following.
In each case, we give the Variable Name and the Variable Value. 

Important: 

- Use Finder to find the exact path as it installed on YOUR machine. 
Your path may be similar, but not exactly like the following. 
- These entries do NOT include \bin at the end - that will be added when we set the Path. 


HADOOP_HOME
C:\Users\YOURNAME\Documents\hadoop

JAVA_HOME
C:\Program Files\Eclipse Adoptium\jdk-17.0.13.11-hotspot

PYSPARK_PYTHON
C:\Users\YOURNAME\AppData\Local\Programs\Python\Python310\python.exe

PYSPARK_DRIVER_PYTHON 
C:\Users\YOURNAME\AppData\Local\Programs\Python\Python310\python.exe

SPARK_HOME
C:\Users\YOURNAME\Documents\spark\spark-3.5.3-bin-hadoop3\spark-3.5.3-bin-hadoop3
  
### Update the System Path 

In the same Environment Variables window, click the **Path** variable under System Variables.

Click "New" to add a new Path entry for the bin folder for each of the following. 
The bin folder is where the binary executable files are kept. 

%HADOOP_HOME%\bin

%JAVA_HOME%\bin

%SPARK_HOME%\bin


## Verify

Restart your machine. 

Open a PowerShell terminal and run the following commands one at a time. 
Be sure a valid version number appears. 
If not, post your results and any error messages in the discussion. 

```shell
java -version
javac -version
py --version
spark-submit --version
```