# Kafka Loader User Guide

## Overview

Kafka is a popular pub-sub system in enterprise IT, offering a distributed and fault-tolerant real-time data pipeline. TigerGraph's Kafka Loader feature lets you easily integrate with a Kafka cluster and speed up your real-time data ingestion. It is easily extensible using the many plugins available in the Kafka ecosystem.

The Kafka Loader consumes data in a Kafka cluster and loads data into the TigerGraph system. 

## Architecture <a id="KafkaLoaderUserDocumentation-Architecture"></a>

From a high level, a user provides instructions to the TigerGraph system through GSQL, and the external Kafka cluster loads data into TigerGraph's RestPP server. The following diagram demonstrates the Kafka Loader data architecture.

![Kafka Data Loader Architecture](../../.gitbook/assets/kafka-loading-architecture.png)

## Prerequisites

You should have a Kafka cluster configured and set up in your environment. 

Once you have the external Kafka cluster setup, you need to prepare the following two configuration files and place them in your desired location in TigerGraph system: 

1. Kafka data source configuration file: This file includes the external Kafka broker's domain name and port. Through the configuration file, TigerGraph system knows the location and port of the external Kafka broker.  Please see an example in [**Step 1. Define the Data Source**](kafka-loader-user-guide.md#KafkaLoaderUserDocumentationDraft-CREATEDATA_SOURCEVariable).
2. Kafka topic and partition configuration file: This file includes the Kafka topic, partition list, and start offset for the loading messages.  Please see an example in [**Step 2. Create a Loading Job**](kafka-loader-user-guide.md#2-create-a-loading-job)**.** 

## Configuring and Using the Kafka Loader <a id="KafkaLoaderUserDocumentation-DataLoadingWorkflow"></a>

There are three basic steps:

1. [Define the data source](kafka-loader-user-guide.md#KafkaLoaderUserDocumentationDraft-CREATEDATA_SOURCEVariable)
2. [Create a loading job](kafka-loader-user-guide.md#2-create-loading-job-statement)
3. [Run the loading job](kafka-loader-user-guide.md#KafkaLoaderUserDocumentationDraft-RunLoadingJobStatement)

The GSQL syntax for the Kafka Loader is designed to be consistent with the existing GSQL loading syntax.  

### 1. Define the Data Source <a id="KafkaLoaderUserDocumentationDraft-CREATEDATA_SOURCEVariable"></a>

#### **CREATE DATA\_SOURCE**

Before starting a Kafka data loading job, you need to define the Kafka server as a data source. The CREATE DATA\_SOURCE statement defines a data\_source variable with a subtype of KAFKA:

```ruby
CREATE DATA_SOURCE KAFKA data_source_name
```

**Kafka Data Source Configuration File**

After the data source is created, then use the SET command to specify the path to a configuration file for that data source. 

```ruby
SET data_source_name = "/path/to/kafka.config"
```

This SET command reads, validates, and applies the configuration file, integrating its settings into TigerGraph's dictionary. The data source configuration file's content, structured as a JSON object, describes the Kafka server's global settings, including the data source ip and port. A sample kafka.conf is shown in the following example:

```text
{
  "broker": "192.168.1.11:9092",
}
```



The "broker" key is required, and its value is composite of a fully qualified domain name \(or IP\) and port. Additional Kafka configuration parameters may be provided \(see Kafka documentation\) by using the optional "kafka\_config" key. For its value, provide a list of key-value pairs. For example:

```text
{
  "broker": "localhost:9092",
  "kafka_config": {"group.id":"tigergraph"}
}
```

For simplicity, you can merge the CREATE DATA\_SOURCE and SET statements:

```ruby
CREATE DATA_SOURCE KAFKA data_source_name = "/path/to/kafka.config"
```

{% hint style="info" %}
1. If you have a TigerGraph cluster, the configuration file must be on machine m1, where the GSQL server and GSQL client both reside,  and it must be in JSON format. If the configuration file uses a relative path, the path should be relative to the GSQL client working directory.
2. Each time when the config file is updated, you must run "SET data\_source\_name"  to update the data source details in the dictionary.
{% endhint %}

To further simplify, instead of specifying the Kafka data source config file path, you can also directly provide the Kafka data source configuration as a string argument, as shown below:

```ruby
CREATE DATA_SOURCE KAFKA data_source_name = "{\"broker\":\"broker.full.domain.name:9092\"}"
```

{% hint style="success" %}
**Tip**: The above simplified statement is useful for using Kafka Data Loader in TigerGraph Cloud. In TigerGraph Cloud \(tgcloud.io\), you can use GSQL web shell to define and create Kafka data sources, without creating the Kafka data source configuration file in filesystem.
{% endhint %}

**ADVANCED: MultiGraph Support**

The Kafka Loader supports the TigerGraph MultiGraph feature. In the MultiGraph context, a data source can be either global or local:

1. A global data source can only be created by a superuser, who can grant it to any graph.
2. An admin user can only create a local data source, which cannot be accessed by other graphs.

The following are examples of permitted DATA\_SOURCE operations.

1. A **superuser** may create a global level data source without assigning it to a particular graph:

```ruby
CREATE DATA_SOURCE KAFKA k1 = "/path/to/config"
```

  2. A **superuser** may grant/revoke a data source to/from one or more graphs:

```ruby
GRANT DATA_SOURCE k1 TO GRAPH graph1, graph2
REVOKE DATA_SOURCE k1 FROM GRAPH graph1, graph2
```

    **3**. ****An **admin** user may create a local data source for a specified graph which they administer:

```ruby
CREATE DATA_SOURCE KAFKA k1 = "/path/to/config" FOR GRAPH test_graph
```

{% hint style="info" %}
In the above statement, the local data\_source k1 is only accessible to graph test\_graph. A superuser cannot grant it to another graph**.**
{% endhint %}

#### DROP DATA\_SOURCE

A data\_source variable can be dropped by a user who has privilege. A global data source can only be dropped by a superuser. A local data\_source can only be dropped by an admin for the relevant graph or by a superuser. The syntax for the DROP command is as follows:

```ruby
DROP DATA_SOURCE <source1>[<source2>...] | * | ALL
```

Below is an example of several legal kafka data\_source create and drop commands.

```ruby
CREATE DATA_SOURCE KAFKA k1 = "/home/tigergraph/kafka.conf"
CREATE DATA_SOURCE KAFKA k2 = "/home/tigergraph/kafka2.conf"
 
DROP DATA_SOURCE k1, k2
DROP DATA_SOURCE *
DROP DATA_SOURCE ALL
```

#### SHOW DATA\_SOURCE

The SHOW DATA\_SOURCE command will display a summary of all existing data\_sources for which the user has privilege:

```c
$ GSQL SHOW DATA_SOURCE *
 
# the sample output
Data Source:
  - KAFKA k1 ("127.0.0.1:9092")
The global data source will be shown in global scope. The graph scope will only show the data source it has access to.
 
```

### 2. Create a Loading Job

The Kafka Loader uses the same basic [CREATE LOADING JOB](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/creating-a-loading-job#create-loading-job) syntax used for standard GSQL loading jobs. A DEFINE FILENAME statement should be used to assign a loader FILENAME variable to a Kafka data source name and the path to its config file.

In addition, the filename can be specified in the RUN LOADING JOB statement with the USING clause. The filename value set by a RUN statement overrides the value set in the CREATE LOADING JOB.

Below is the syntax for DEFINE FILENAME for use with the Kakfa Loader. In the syntax, $DATA\_SOURCE\_NAME is the Kafka data source name, and the path points to a configuration file with topic and partition information of the Kafka server. The Kafka configuration file must be in JSON format.

```ruby
DEFINE FILENAME filevar "=" [filepath_string | data_source_string]; 
data_source_string = $DATA_SOURCE_NAME":"<path_to_configfile>
```

_**Example:**_ Load a Kafka Data Source _****_**k1**, _****_where the path to the topic-partition configuration file is "~/topic\_partition1.conf":

```ruby
DEFINE FILENAME f1 = "$k1:~/topic_partition1.conf";
```

**Kafka Topic-Partition Configuration File**

The topic-partition configuration file tells the TigerGraph system exactly which Kafka records to read.  Similar to the data source configuration file described above, the contents are in JSON object format. An example file is shown below:

{% code title="topic\_partition1.conf" %}
```yaml
{
  "topic": "topicName1",
  "partition_list": [
    {
      "start_offset": -1,
      "partition": 0
    },
    {
      "start_offset": -1,
      "partition": 1
    },
    {
      "start_offset": -1,
      "partition": 2
    }
  ]
}
```
{% endcode %}

The "topic" key is required. Optionally,  a "partition\_list" array can be included to specify which topic partitions to read and what start offsets to use.  If the "partition\_list" key is missing or empty, all partitions in this topic will be used for loading. The default offset for loading is "-1", which means you will load data from the most recent message in the topic, i.e., the end of the topic. If you want to load from the beginning of a topic, the "start\_offset" value should be "-2". 

You can also overwrite the default offset by setting "default\_start\_offset" in the Kafka topic configuration file. For example, 

```yaml
# all partition will be used if no "partition_list" item
{
  "topic": "topicName1"
}
 
# with empty "partition_list"
{
  "topic": "topicName1",
  "partition_list": []
}
 
# overwrite the default start offset
{
  "topic": "topicName1",
  "default_start_offset", 0
}
```

Instead of specifying the config file path, you can also directly provide the topic-partition configuration as a string argument, as shown below:

```text
DEFINE FILENAME f1 = "$k1:~/topic_partition_config.json";
DEFINE FILENAME f1 = "$k1:{\"topic\":\"zzz\",\"default_start_offset\":2,\"partition_list\":[]}";
```

### 3. Run the Loading Job <a id="KafkaLoaderUserDocumentationDraft-RunLoadingJobStatement"></a>

The Kafka Loader uses the same [RUN LOADING JOB](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/running-a-loading-job#run-loading-job) statement that is used for GSQL loading from files. Each filename variable can be assigned a string "DATA\_SOURCE Var:topic\_partition configure", which will override the value defined in the loading job. In the example below, the config files for f3 and f4 are being set by the RUN command, whereas f1 is using the config which was specified in the CREATE LOADING JOB statement.

```ruby
RUN LOADING JOB job1 USING f1, f3="$k1:~/topic_part3.config", f4="$k1:~/topic_part4.config", EOF="true";
```

{% hint style="warning" %}
A RUN LOADING JOB instance may only use one type of data source.  E.g., you may not mix both Kafka data sources and regular file data sources in one loading job.
{% endhint %}

All filename variables in one loading job statement must refer to the same DATA\_SOURCE variable.

There are two modes for the Kafka Loader: streaming mode and EOF mode. The default mode is streaming mode.  In streaming mode, loading will never stop until the job is aborted. In EOF mode,  loading will stop after consuming the current Kafka message.

To set EOF mode, an optional parameter is added to the RUN LOADING JOB syntax:

```ruby
RUN LOADING JOB [-noprint] [-dryrun] [-n [i],j] jobname
   [ USING filevar [="filepath_string"][, filevar [="filepath_string"]]*
   [, CONCURRENCY="cnum"][,BATCH_SIZE="bnum"]][, EOF="true"]
```

## Manage Loading Jobs

Kafka Loader loading jobs are managed the same way as native loader jobs. The three key commands are 

* SHOW LOADING STATUS
* ABORT LOADING JOB
* RESUME LOADING JOB

For example, the syntax for the SHOW LOADING STATUS command is as follows:

```ruby
SHOW LOADING STATUS job_id|ALL
```

To refer to a specific job instance, using the job\_id which is provided when RUN LOADING JOB is executed. For each loading job, the above command reports the following information :

1. current loaded offset for each partition
2. average loading speed
3. loaded size
4. duration

See [Inspecting and Managing Loading Jobs](https://docs.tigergraph.com/dev/gsql-ref/ddl-and-loading/running-a-loading-job#inspecting-and-managing-loading-jobs) for more details.

## Kafka Loader Example

Here is an example code for loading data through Kafka Loader:

```ruby
USE GRAPH test_graph
DROP JOB load_person
DROP DATA_SOURCE k1
 
#create data_source kafka k1 = "kafka_config.json" for graph test_graph
CREATE DATA_SOURCE KAFKA k1 FOR GRAPH test_graph
SET k1 = "kafka_config.json"
 
# define the loading jobs
CREATE LOADING JOB load_person FOR GRAPH test_graph {
  DEFINE FILENAME f1 = "$k1:topic_partition_config.json";
  LOAD f1
      TO VERTEX Person VALUES ($2, $0, $1),
      TO EDGE Person2Comp VALUES ($0, $1, $2)
      USING SEPARATOR=",";
}
 
# load the data
RUN LOADING JOB load_person
```

##   

