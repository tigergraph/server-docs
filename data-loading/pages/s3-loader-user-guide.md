# AWS S3 Loader User Guide

## Overview

AWS Simple Storage Service \(S3\) is a popular destination to store data in the cloud and has become an essential component in the data pipeline of many enterprises. It is an object storage service on the AWS platform which can be accessed through a web service interface. 

TigerGraph's S3 Loader makes it easier for you to integrate with an Amazon S3 service and ingest data from S3 buckets either in _realtime_ or via _one-time data import_ into the TigerGraph System. Your TigerGraph cluster can be deployed either on-premises or in a cloud environment.

## Architecture

From a high level, a user provides instructions to the TigerGraph system through GSQL, and the external Amazon S3 data is loaded into TigerGraph's RESTPP server. The following diagram demonstrates the S3 Loader data architecture.

![](../../.gitbook/assets/graphguru15-image1.png)

## **Prerequisites**

You should have uploaded your data to Amazon S3 buckets.

Once you have the buckets set up, you need to prepare the following two configuration files and place them in your desired location in the TigerGraph system:

1. S3 data source configuration file: This file includes the credentials for accessing Amazon S3 which consists of _access key_ and _secret key_. Through the configuration file, the TigerGraph system acquires the authority to access your buckets. Please see the example in [Step 1. Define the Data Source](s3-loader-user-guide.md#1-define-the-data-source).
2.  S3 file configuration file: This file specifies various options for reading data from Amazon S3. Please the see example in [Step 2. Create a Loading Job](s3-loader-user-guide.md#2-create-a-loading-job).

## Configuring and Using the S3 Loader

There are three basic steps:

1. [Define the Data Source](s3-loader-user-guide.md#1-define-the-data-source)
2. [Create a Loading Job](s3-loader-user-guide.md#2-create-a-loading-job)
3. [Run the Loading Job](s3-loader-user-guide.md#3-run-the-loading-job)

The GSQL syntax for the S3 Loader is designed to be consistent with the existing GSQL loading syntax.  

### 1. Define the Data Source

#### CREATE DATA\_SOURCE

Before starting a S3 data loading job, you need to define the credentials to connect to Amazons  S3. The CREATE DATA\_SOURCE statement defines a data\_source type variable, with a sub type S3:

```ruby
CREATE DATA_SOURCE S3 data_source_name
```

#### S3 Data Source Configuration File

After the data source is created, use the SET command to specify the path to a configuration file for that data source.

```ruby
SET data_source_name = "/path/to/s3.config";
```

This SET command reads, validates, and applies the configuration file, integrating its settings into TigerGraph's dictionary. The data source configuration file's content, structured as a JSON object, describes the S3 credential settings, including the _access key_ and _secret key_. A sample s3.config is shown in the following example:

{% code title="s3.config" %}
```typescript
{
    "file.reader.settings.fs.s3a.access.key": "AKIAJ****4YGHQ",
    "file.reader.settings.fs.s3a.secret.key": "R8bli****p+dT4"
}
```
{% endcode %}

For simplicity, you can merge the CREATE DATA\_SOURCE and SET statements:

```ruby
CREATE DATA_SOURCE S3 data_source_name = "/path/to/s3.config"
```

{% hint style="info" %}
1. If you have a TigerGraph cluster, the configuration file must be on machine m1, where the GSQL server and GSQL client both reside,  and it must be in JSON format. If the configuration file uses a relative path, the path should be relative to the GSQL client working directory.
2. Each time when the config file is updated, you must run "SET data\_source\_name"  to update the data source details in the dictionary.
{% endhint %}

To further simplify, instead of specifying the S3 data source config file path, you can also directly provide the S3 data source configuration as a string argument, as shown below:

```ruby
CREATE DATA_SOURCE S3 data_source_name = "{\"file.reader.settings.fs.s3a.access.key\":\"AKIAJ****4YGHQ\",\"file.reader.settings.fs.s3a.secret.key\":\"R8bli****p+dT4\"}"
```

{% hint style="success" %}
**Tip**: The above simplified statement is useful for using S3 Data Loader in TigerGraph Cloud when you are not loading S3 data through GraphStudio. In TigerGraph Cloud \(tgcloud.io\), you can also use GSQL web shell to define and create S3 data sources, without creating the S3 data source configuration file in filesystem.
{% endhint %}

#### ADVANCED: MultiGraph Support

The S3 Loader supports the TigerGraph MultiGraph feature. In the MultiGraph context, a data source can be either global or local:

1. A global data source can only be created by a superuser, who can grant the global data source to any graph.
2. An admin user can only create a local data source, which cannot be accessed by other graphs.

The following are examples of permitted DATA\_SOURCE operations.

1. A **superuser** may create a global level data source without assigning it to a particular graph:

```ruby
CREATE DATA_SOURCE S3 s1 = "/path/to/config"
```

    2. A **superuser** may grant/revoke a data source to/from one or more graphs:

```ruby
GRANT DATA_SOURCE s1 TO GRAPH graph1, graph2
REVOKE DATA_SOURCE s1 FROM GRAPH graph1, graph2
```

    3. An **admin** user may create a local data source for a specified graph which the admin user administers:

```ruby
CREATE DATA_SOURCE S3 s1 = "/path/to/config" FOR GRAPH test_graph
```

{% hint style="info" %}
In the above statement, the local data\_source s1 is only accessible to graph test\_graph. A superuser cannot grant it to another graph**.**
{% endhint %}

#### DROP DATA\_SOURCE

A data\_source variable can be dropped by a user who has the privilege. A global data source can only be dropped by a superuser. A local data\_source can only be dropped by an admin for the relevant graph or by a superuser. The syntax for the DROP command is as follows:

```ruby
DROP DATA_SOURCE <source1>[<source2>...] | * | ALL
```

Below is an example with a few legal s3 data\_source create and drop commands.

```coffeescript
CREATE DATA_SOURCE S3 s1 = "/home/tigergraph/s3.config"
CREATE DATA_SOURCE S3 s2 = "/home/tigergraph/s3_2.config"
 
DROP DATA_SOURCE s1, s2
DROP DATA_SOURCE *
DROP DATA_SOURCE ALL
```

#### SHOW DATA\_SOURCE

The SHOW DATA\_SOURCE command will display a summary of all existing data\_sources for which the user has privilege:

```bash
$ GSQL SHOW DATA_SOURCE *
 
# The sample output:
Data Source:
  - S3 s1 ("file.reader.settings.fs.s3a.access.key": "AKIAJ****4YGHQ", "file.reader.settings.fs.s3a.secret.key": "R8bli****p+dT4")
# The global data source will be shown in global scope.
# The graph scope will only show the data source it has access to.
```

### 2. Create a Loading Job

The S3 Loader uses the same basic [CREATE LOADING JOB](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/creating-a-loading-job#create-loading-job) syntax used for standard GSQL loading jobs. A DEFINE FILENAME statement should be used to assign a loader FILENAME variable to a S3 data source name and the path to its config file.

In addition, the filename can be specified in the RUN LOADING JOB statement with the USING clause. The filename value set by a RUN statement overrides the value set in the CREATE LOADING JOB.

Below is the syntax for DEFINE FILENAME when using the S3 Loader. In the syntax, $DATA\_SOURCE\_NAME is the S3 data source name, and the path points to a configuration file _which provides information about how to read an Amazon S3 file_. The S3 file configuration file must be in JSON format.

```ruby
DEFINE FILENAME filevar "=" [filepath_string | data_source_string]; 
data_source_string = $DATA_SOURCE_NAME":"<path_to_configfile>
```

_**Example:**_ Load a S3 Data Source _**s**_**1**, _****_where the path to the file configuration file is "~/files.conf":

```ruby
DEFINE FILENAME f1 = "$s1:~/files.config";
```

#### S3 File Configuration File

The S3 file configuration file tells the TigerGraph system exactly which Amazon S3 files to read and how to read them. Similar to the data source configuration file described above, the contents are in JSON object format. An example file is shown below.

{% code title="files.config" %}
```typescript
{
    "file.uris": "s3://my-bucket/data.csv"
}
```
{% endcode %}

The "file.uris" key is required. It specifies one or more paths on your Amazon S3 bucket. Each path is either to an individual file or to a directory. If it is a directory, then each file directly under that directory is included. You can specify multiple paths by using a comma-separated list. An example with multiple paths is show below:

{% code title="files.config" %}
```typescript
{
    "file.uris": "s3://my-bucket1/data1.csv,s3://my-bucket1/data2.csv,s3://my-bucket2/data3.csv"
}
```
{% endcode %}

Instead of specifying the config file path, you can also directly provide the S3 file configuration as a string argument, as shown below:

```ruby
DEFINE FILENAME f1 = "$s1:~/files.config";
DEFINE FILENAME f1 = "$s1:{\"file.uris\":\"s3://my-bucket/data.csv\"}";
```

#### ADVANCED: Configure How to Read S3 File

Besides the required "file.uris" key, you can further configure the S3 loader. A sample full configuration is shown below:

{% code title="files.config" %}
```typescript
{
    "tasks.max": 1,
    "file.uris": "s3://my-bucket/data.csv",
    "file.regexp": ".*",
    "file.recursive": false,
    "file.scan.interval.ms": 60000,
    "file.reader.type": "text",
    "file.reader.batch.size": 10000,
    "file.reader.text.archive.type": "auto",
    "file.reader.text.archive.extensions.tar": "tar",
    "file.reader.text.archive.extensions.zip": "zip",
    "file.reader.text.archive.extensions.gzip": "tar.gz,tgz"
}
```
{% endcode %}

Following is a detailed explanation of each option:

* "**tasks.max**" \(default is **1**\): specifies the maximum number of tasks which can run in parallel. E.g. if there are 2 files and 2 tasks, each task will handle 1 file. If there are 2 files and 1 task, the single task will handle 2 files. If there is 1 file and 2 tasks, one of the tasks will handle the file.
* "**file.uris**": specifies the path\(s\) to the data files on Amazon S3. The path can also be dynamic by using expressions to modify the URIs at runtime. These expressions have the form `${XX}` where XX represents a pattern from [`DateTimeFormatter`](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html) Java class.

{% hint style="info" %}
if you want to ingest data dynamically, i.e. directories/files created every day and avoid adding new URIs every time, you can include expressions in URIs to do that. For example, for the URI`s3://my-bucket/${yyyy}`, it is converted to`s3://my-bucket/2019`when running the loader. You can use as many as you like in the URIs, for instance:`s3://my-bucket/${yyyy}/${MM}/${DD}/${HH}-${mm}`
{% endhint %}

* "**file.regexp**" \(default is **.\*** which matches all files\): the regular expression to filter which files to read. 
* "**file.recursive**" \(default is **false**\): whether to recursively access all files in a directory.
* "**file.scan.interval.ms**" \(default is **60000**\): the wait time in ms before starting another scan of the file directory after finishing the current scan. Only applicable in **stream** mode.
* "**file.reader.type**" \(default is **text**\): the type of file reader to use. If **text**, read the file line by line as pure text. If **parquet**, read the file as parquet format.
* "**file.reader.batch.size**" \(default is **1000**\): maximum number of lines to include in a single batch.
* "**file.reader.text.archive.type**" \(default is **auto**\): the archive type of the file to be read. If **auto**, determine the archive type automatically. If **tar**, read the file with tar format. if **zip**, read the file with zip format. If **gzip**, read the file with gzip format. If **none**, read the file normally.
* "**file.reader.text.archive.extensions.tar**" \(default is **tar**\): the list of file extensions to be read with tar format.
* "**file.reader.text.archive.extensions.zip**" \(default is **zip**\):  ****the list of file extensions to be read with zip format.
* "**file.reader.text.archive.extensions.gzip**" \(default is **gzip**\): the list of file extensions to be read with gzip format.

{% hint style="info" %}
The archive type is applied to all files in "file.uris" when loading. If you have different archive type files to be read at the same time, set **auto** for "file.reader.text.archive.type" and configure how to detect each archive extensions by providing the extensions list. Currently we support **tar**, **zip** and **gzip** archive types.
{% endhint %}

### 3. Run the Loading Job

The S3 Loader uses the same [RUN LOADING JOB](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/running-a-loading-job#run-loading-job) statement that is used for GSQL loading from files. Each filename variable can be assigned a string "DATA\_SOURCE Var:file configure", which will override the value defined in the loading job. In the example below, the config files for f2 and f3 are being set by the RUN command, whereas f1 is using the config which was specified in the CREATE LOADING JOB statement.

```ruby
RUN LOADING JOB job1 USING f1, f2="$s1:~/files1.config", f3="$s2:~/files2.config", EOF="true";
```

{% hint style="warning" %}
A RUN LOADING JOB instance may only use one type of data source.  E.g., you may not mix both S3 data sources and regular file data sources in one loading job.
{% endhint %}

All filename variables in one loading job statement must refer to the same DATA\_SOURCE variable.

There are two modes for the S3 Loader: **streaming** mode and **EOF** mode. The default mode is **streaming** mode. In **streaming** mode, loading will never stop until the job is aborted. In **EOF** mode,  loading will stop after consuming the provided Amazon S3 file objects.

To set **EOF** mode, an optional parameter is added to the RUN LOADING JOB syntax:

```ruby
RUN LOADING JOB [-noprint] [-dryrun] [-n [i],j] jobname
   [ USING filevar [="filepath_string"][, filevar [="filepath_string"]]*
   [, CONCURRENCY="cnum"][,BATCH_SIZE="bnum"]][, EOF="true"]
```

## Manage Loading Jobs

S3 Loader loading jobs are managed the same way as native loader jobs. The three key commands are 

* SHOW LOADING STATUS
* ABORT LOADING JOB
* RESUME LOADING JOB

For example, the syntax for the SHOW LOADING STATUS command is as follows:

```ruby
SHOW LOADING STATUS job_id|ALL
```

To refer to a specific job instance, use the job\_id which is provided when RUN LOADING JOB is executed. For each loading job, the above command reports the following information :

1. current loaded lines
2. average loading speed
3. loaded size
4. duration

See [Inspecting and Managing Loading Jobs](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/running-a-loading-job#inspecting-and-managing-loading-jobs) for more details.

## S3 Loader Example

Here is an example code for loading data through the S3 Loader:

```ruby
USE GRAPH test_graph
DROP JOB load_person
DROP DATA_SOURCE s1
 
# Create data_source s3 s1 = "s3_config.json" for graph test_graph.
CREATE DATA_SOURCE S3 s1 FOR GRAPH test_graph
SET s1 = "s3_config.json"
 
# Define the loading jobs.
CREATE LOADING JOB load_person FOR GRAPH test_graph {
  DEFINE FILENAME f1 = "$s1:s3_file_config.json";
  LOAD f1
      TO VERTEX Person VALUES ($2, $0, $1),
      TO EDGE Person2Comp VALUES ($0, $1, $2)
      USING SEPARATOR=",";
}
 
# load the data
RUN LOADING JOB load_person
```

