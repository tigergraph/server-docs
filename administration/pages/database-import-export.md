---
description: 'Export/Import is a complement to Backup/Restore, not a substitute.'
---

# Database Import/Export

## Introduction

The GSQL EXPORT and IMPORT commands perform a logical backup and restore. A database export contains the database's data, and optionally some types of metadata, which can be subsequently imported in order to recreate the same database, in the original or in a different TigerGraph platform instance.

{% hint style="danger" %}
Known Issues \(Updated Feb 16th\):

* User-defined loading jobs containing[`DELETE` statements](../../../dev/gsql-ref/ddl-and-loading/creating-a-loading-job.md#delete-statement) are not exported correctly.
* If a graph contains vertex or edge types with a composite key, the graph data is exported in a nonstandard format which cannot be reimported.
{% endhint %}

## EXPORT GRAPH

Available to the superuser role only.

The EXPORT GRAPH command reads the data and metadata for one or more graphs and writes the information to a zip file in the designated folder.  If no options are specified, then a full backup is performed, including schema, data, template information, and user profiles.

{% tabs %}
{% tab title="Syntax" %}
```text
EXPORT GRAPH ALL [exportOptions] TO "/path/to/a/folder"

exportOptions ::=
(-S | --SCHEMA | -T | --TEMPLATE | -D | --DATA | -U | --USERS | -P | --PASSWORD pwd)

    -S, --SCHEMA        Only Schema will be exported
    -T, --TEMPLATE      Only Schema, Queries, Loading Jobs, UDFs
    -D, --DATA          Only Data Sources will be exported
    -U, --USERS         Includes Permissions, Secrets, and Tokens
    -P, --PASSWORD      Encrypt with password. User will be prompted.
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
NOTE: The export directory should be empty before running EXPORT GRAPH because all contents are zipped and compressed.
{% endhint %}

The current version exports ALL graphs in a MultiGraph system.  A future version of EXPORT GRAPH will allow the user to select which graphs to export. 

The export contains four categories of files:

1. Data files in csv format, one file for each type of vertex and each type of edge.
2. GSQL DDL command files created by the export command.  The import command uses these files to recreate the graph schema\(s\) and reload the data.
3. Copies of the database's queries, loading jobs, and user-defined functions.
4. GSQL command files used to recreate the users and their privileges.

The following files are created in the specified directory when exporting and are then zipped into a single file called ExportedGraphs.zip.

{% hint style="warning" %}
If the file is password-protected, it can only be unzipped using GSQL IMPORT. The security feature prevents users from directly unzipping it.
{% endhint %}

* A **DBImportExport\_&lt;graphName&gt;.gsql** for each graph called &lt;graphName&gt; in a multigraph database that contains a series of GSQL DDL statements that do the following:
  * Create the exported graph, along with its local vertex, edge, and tuple types,
  * Create the loading jobs from the exported graphs
  * Create data source file objects
  * Create queries 
* A **graph\_&lt;graphName&gt;/** folder for each graph in a multigraph database containing data for local vertex/edge types in &lt;graphName&gt;. For each vertex or edge type called &lt;type&gt;, there is one of the following two data files:
  * vertex\_&lt;type&gt;.csv
  * edge\_&lt;type&gt;.csv
* **global.gsql** - DDL job to create all global vertex and edge types, and data sources.
* **tuple.gsql** - DDL job to create all User Defined Tuples.
* Exported data and jobs used to restore the data:
  * **GlobalTypes/** - folder containing data for global vertex/edge types
    * vertex\_name.csv
    * edge\_name.csv
  * **run\_loading\_jobs.gsql** - DDL created by the export command which will be used during import:
    * Temporary global schema change job to add user-defined indexes. This schema job is dropped after it is has run.
    * Loading jobs to load data for global and local vertex/edges.
* Database's saved queries, loading jobs, and schema change jobs
  * **SchemaChangeJob/ -** folder containing DDL for schema change jobs. See section "Schema Change Jobs" for more information

    * Global\_Schema\_Change\_Jobs.gsql contains all global schema change jobs
    * graphName\_Schema\_Change\_Jobs.gsql contains schema change jobs for each graph "graphName"

    **Tokenbank.cpp** - copy of `<tigergraph.root.dir>/app/<VERSION_NUM>/dev/gdk/gsql/src/TokenBank/TokenBank.cpp`

  * **ExprFunctions.hpp** - copy of `<tigergraph.root.dir>/app/<VERSION_NUM>dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp`
  * **ExprUtil.hpp** - copy of `<tigergraph.root.dir>/app/<VERSION_NUM>/dev/gdk/gsql/src/QueryUdf/ExprUtil.hpp`
* Users:
  * **users.gsql** - DDL to create all exported users and import Secrets and Tokens, and grant permissions.

{% tabs %}
{% tab title="Example" %}
```text
EXPORT GRAPH ALL TO "/tmp/export_graphs/"
```
{% endtab %}
{% endtabs %}

### Insufficient Disk Space

If not enough disk space is available for the data to be exported, the system returns an error message indicating not all data has been exported. Some data may have already been written to disk. If an insufficient disk error occurs, the files will not be zipped, due to the possibility of corrupted data which would then corrupt the zip file. The user should clear enough disk space, including deleting the partially exported data, before reattempting the export.

{% hint style="warning" %}
It is possible for all the files to be written to disk and then to run out of disk space during the zip operation. If that is the case, the system will report this error. The unzipped files will be present in the specified export directory.
{% endhint %}

### Default Timeout and Session Parameter export\_timeout

If timeout is reached during export, the system returns an error message indicating not all data has been exported. Some data may have already been written to disk. If an insufficient disk error occurs, the files will not be zipped, due to the possibility of corrupted data which would then corrupt the zip file. The user should increase the timeout, and then rerun the export.

The timeout limit is controlled by the session parameter **export\_timeout**.  The default timeout is ~138 hours. The change the timeout limit, use the command:

```text
set export_timeout = <timeout_in_ms>
```

## IMPORT GRAPH

Available to the superuser role only.

The IMPORT GRAPH command unzips the .zip file ExportedGraph.zip located in the designated folder, unzips it, and then runs the GSQL command files within.

{% tabs %}
{% tab title="Syntax" %}
```text
IMPORT GRAPH ALL [importOptions] FROM "/path/from/a/folder"

importOptions ::= [-P | --PASSWORD ] [ (-KU | -- keep-users]
    -P,  --PASSWORD     Decrypt with password. User will be prompted.
    -KU, --KEEP-USERS   Do not delete user identities before importing
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Example" %}
```text
IMPORT GRAPH ALL FROM "/tmp/export_graphs/"
```
{% endtab %}
{% endtabs %}

{% hint style="danger" %}
WARNING: IMPORT GRAPH looks for specific filenames.  If either the zip file or any of its contents are renamed by the user, IMPORT GRAPH may fail.
{% endhint %}

{% hint style="danger" %}
WARNING: IMPORT GRAPH erases the current database \(equivalent to running DROP ALL\). The current version does not support incremental or supplemental changes to an existing database \(except for the --keep-users option\)
{% endhint %}

### Loading Jobs

There are two sets of loading jobs:

1. Those that were in the **catalog** of the database which was exported. These are embedded in the file DBImportExport\_graphName.gsql
2. Those that are **created by EXPORT GRAPH** and are used to assist with the import process. These are embedded in the file run\_loading\_jobs,gsql.

The catalog loading jobs are not needed to restore the data. They are included for archival purpose.

{% hint style="warning" %}
Some special rules apply to importing loading jobs. Some catalog loading jobs will not be imported.
{% endhint %}

1. **If a catalog loading job contains `DEFINE FILENAME F = "/path/to/file/"`**, the path will be removed and the imported loading job will only contain **`DEFINE FILENAME F`**.  This is to allow a loading job to still be imported even though the file may no longer exist or the path may be different due to moving to another TigerGraph instance. 
2. **If a specific file path is used directly in the LOAD statement, and the file cannot be found, the loading job cannot be created and will be skipped.**  For example, `LOAD "/path/to/file" to vertex v1` cannot be created if `/path/to/file` does not exist. 
3. **Any file path using `$sys.data_root` will be skipped.** This is because the value of `$sys.data_root` is  not retained from export. During import, `$sys.data_root` is set to the root folder of the import location. 

### Schema Change Jobs

There are two sets of schema change jobs:

1. Those that were in the catalog of the database which was exported. These are stored in the folder /SchemaChangeJobs.
2. Those that were created by EXPORT GRAPH and are used to assist with the import process.  These are in the run\_loading\_jobs.gsql command file.  The jobs are dropped after the import command is finished with them.

The database's schema change jobs are not executed during the import process. This is because if a schema change job had been run before the export, then the exported schema already reflects the result of the schema change job. The directory /SchemaChangeJobs contains these files:

* **Global\_Schema\_Change\_Jobs.gsql** contains all global schema change jobs
* **&lt;graphName&gt;\_Schema\_Change\_Jobs.gsql** contains schema change jobs for each graph &lt;graphName&gt;.

## Cluster Mode

In v3.0, importing and exporting clusters is not fully automated. The database can be exported and imported by following some additional steps.

### Export from a Cluster

Rather than creating a single export zip file, export will create a file for each machine. Before exporting, specific folders must be created on each server using the following commands:

{% tabs %}
{% tab title="Run on each server before EXPORT" %}
```text
grun all "mkdir -p /path/to/export_directory/GlobalTypes/"
grun all "mkdir -p /path/to/export_directory/graph_<graphName>/"
```
{% endtab %}
{% endtabs %}

Then run the export command on one server. The EXPORT command does not bundle all the files to one server, and it does not compress each server's files to one zip. Some files, including the data files, will be exported to each server, to the folders created above. Some files will be only on the local server where EXPORT GRAPH was run. 

### Import to a Cluster

#### 1. Place the files on the import servers

You may only import to a cluster that has the same number and configuration of servers as the data from which the export originated. **Transfer the files from one export server to a corresponding import server.** That is, copy the files from  
`export_server_n:/path/to/export_directory` to  
`import_server_n:/path/to/import/directory`

2. Manually modify the loading jobs

On the main server, edit the run\_loading\_jobs.gsql files as follows.

Find the line\(s\) of the form:  
`LOAD "sys.data_root/.../<vertex_or_edge_type>.csv"`  
Close to it should be similar line that is commented out which have the "all:" data source directive:  
`#LOAD "all:sys.data_root/.../<vertex_or_edge_type>.csv"`

See the example below:

```text
LOAD "$sys.data_root/graph_graph1/localE.csv"
#If running on a cluster, check that the file exists on all nodes then uncomment the line below and comment the line above.
#LOAD "all:$sys.data_root/graph_graph1/localE.csv"
    TO EDGE localE VALUES ($"from", $"to") USING SEPARATOR = "^]", HEADER = "true";
```

**Comment out the LOAD line and uncomment the LOAD all: line**. Be sure that you do this for all data source files.

3. Run the IMPORT GRAPH command from the main server \(e.g., the one that corresponds to the server where EXPORT GRAPH was run\).

