# High Availability Support for GSQL Server

## **Introduction:**

By Design, TigerGraph has built-in HA for all the internal critical components from the beginning. This includes GPE, GSE, REST API Servers, etc. However, the user-facing applications \(GSQL and GraphStudio\) were designed to be set up by customers based on their High Availability \(HA\) needs. This included building solutions using non-TigerGraph components.  With 3.1 release, TigerGraph will support native HA functionality for user-facing applications as well. This simplifies and streamlines HA deployment for users completely. For Operations personnel, this will reduce the operational overhead while enhancing the availability for end users.

## **Overview of the design:**

Before we elaborate the design, we need to understand the topology of how TigerGraph services are deployed in a cluster. TigerGraph nodes in a cluster are organized as ‘m1’, ‘m2’, and so on. Although all nodes in the cluster serve the same function - store data and participate in query execution, m1 is a special node. GSQL server runs on this node to address critical services such as storing client metadata as well as managing connections between client and server. With this feature, m1 will no longer serve as the only node for GSQL server connections. In the new design, other nodes will run standby GSQL servers to provide high availability for client connections.

![](https://lh4.googleusercontent.com/pdt7MlbufmHMFuwTRX3LJev_aZjl0EgSu6XrfpNX8n2TpWSG8UFV2vS3mYSx-OO1opf_gFKCgFb3YDH6fQXMld-Zots3yApywDFBGmfFwlBVKR31bpAWdjrSmV8uegxe1WcchGFJ)

### **Role of Primary GSQL server**

In the 3.1 release, primary GSQL server will continue to perform all the tasks handled by GSQL server prior to 3.1 release. This includes:

1. Process client connections
2. Querying requests from GSQL clients
3. User management requests including token management

In addition to these, when Primary fails, a standby server will switch to become the Primary server, and when the old Primary server is back to normal function, it will become a GSQL Standby server.

### **Role of Standby GSQL Servers**

1. Redirect requests to Primary Server 
2. Help Primary server to check for source data file existence and parse file header \(if ANY is chosen\)

### **Role of GSQL Client**

There is no change in how GSQL Client works.

## **User Impact and Changes:**

### **User Source Code Maintenance**

Users store the following data on m1 node that is needed for query execution:

* GSQL loader's Token functions
* ExprFunctions 
* ExprUtil

This is part of the user source code that TigerGraph system uses to compile. Prior to 3.1 release, this information is available to GSQL server only on m1 node. Typically, users can modify these files directly on the machine. But with HA, the Primary GSQL may not be in m1, and can be switched to any other machine at any time. Users have to make sure all the machines have the same content whenever there are updates to the files. This is a new requirement for users. 

GSQL server will retrieve the User source code files in the following priority order when it needs them:

* Via github/github enterprise \(if configuration is set\),
* Files uploaded via PUT,
* Default files that are shipped with the product

#### **User source code in github code repository**

This requires public network access, or github enterprise server access. User need to provide the following gadmin configuration:

```text
GSQL.GithubUserAcessToken # the credential, or "anonymous", empty means not using github
GSQL.GithubRepository     # e.g. tigergraph/ecosys
GSQL.GithubBranch         # optional, o/w use "master" branch, e.g. demo_github
GSQL.GithubPath           # path to the directory in the github that has TokenBank.cpp, ExprFunctions.hpp, ExprUtil.hpp, e.g. sample_code/src
GSQL.GithubUrl            # optional, used for github enterprise, e.g. https://api.github.com
```

**Example:**

```text
gadmin config set GSQL.GithubUserAcessToken anonymous
gadmin config set GSQL.GithubRepository tigergraph/ecosys
gadmin config set GSQL.GithubBranch demo_github
gadmin config set GSQL.GithubPath sample_code/src
gadmin config apply
```

When GSQL server needs to compile the files, it will retrieve them from github if the GitHub access is configured as above. It will retry 3 times, with timeout=5s for each time. If the connection fails, it will go to the next priority level method, i.e. file uploaded via PUT.

#### **User Source code maintenance for local files in the cluster:**

We are introducing new GSQL commands to address this need. These commands will allow users to upload and download the user source files.

**Upload source code**

```text
PUT TokenBank FROM "path/to/a/file"
PUT ExprFunctions FROM "path/to/a/file"
PUT ExprUtil FROM "path/to/a/file"
```

**Example:**

```text
temp_TokenBank=$tempDir/tmp_TokenBank.cpp
temp_ExprFunctions=$tempDir/tmp_ExprFunctions.hpp
temp_ExprUtil=$tempDir/tmp_ExprUtil.hpp

eval gsql 'PUT TokenBank FROM \"$temp_TokenBank\"'
eval gsql 'PUT ExprFunctions FROM \"$temp_ExprFunctions\"'
eval gsql 'PUT ExprUtil FROM \"$temp_ExprUtil\"'
```

**Download source code**

```text
GET TokenBank TO "path/to/a/file"
GET ExprFunctions TO "path/to/a/file"
GET ExprUtil TO "path/to/a/file"
```

**Example:**

```text
temp_TokenBank2=$tempDir/tmp_TokenBank_2.cpp
temp_ExprFunctions2=$tempDir/tmp_ExprFunctions_2.hpp
temp_ExprUtil2=$tempDir/tmp_ExprUtil_2.hpp

echo "GET TokenBank.cpp, ExprFunctions.hpp and ExprUtil.hpp to current node."

eval gsql 'GET TokenBank TO \"$temp_TokenBank2\"'
eval gsql 'GET ExprFunctions TO \"$temp_ExprFunctions2\"'
eval gsql 'GET ExprUtil TO \"$temp_ExprUtil2\"'
```

The uploaded files will be saved to all nodes. Users will need to have either ‘superuser’ and ‘global\_designer’ roles to have the sufficient privileges to run the PUT/GET commands.

When calling GET command, the user can download the corresponding file from the Primary node, to a local directory at the current cluster node.

When calling PUT command, the local file will be copied to all of the cluster nodes, including itself.

**Example usage scenario to update of the files is as follows:**

```text
// Download the current file via GET, or create a new file from draft;
GET TokenBank TO "/myFolder/file.cpp"
// Upload the file via PUT
PUT TokenBank FROM "/myFolder/file.cpp"
```

For each cluster node, TokenBank.cpp is stored at:

```text
 $(gadmin config get System.DataRoot)/gsql/tokenbank/
```

ExprFunctions.hpp and ExprUtil.hpp files are stored at:

```text
 $(gadmin config get System.DataRoot)/gsql/udf/
```

Full path should be provided including the file name for PUT/GET, eg: 

```text
put ExprFunctions from "/home/path/tmp/ExprFunc.hpp"
get TokenBank to "doc/path/tmp/myTB.cpp"
```

Notice that in the first command, we use absolute path, while in the second command, we use relative path. Both are supported. But “~” is not supported \(eg: “~/tmp/x.hpp”\).

Additionally, users can also use the commands in the following manner as well:

* Use a folder name, and automatically default name will be added. For example:

```text
put ExprFunctions from "/home/path/tmp"
```

It will use ExprFunctions.hpp under the directory "/home/path/tmp" for PUT.

```text
get TokenBank to "home/path/tmp/"
```

It will create/overwrite the file "home/path/tmp/TokenBank.cpp".

If the file name is given in the path, its file extension must be consistent with the corresponding file. For example:

```text
put ExprFunctions from "/home/path/tmp/test1.gsql"
```

is not allowed, since PUT/GET ExprFunctions must use “.hpp” as file extension.

#### **Default file shipped with TigerGraph package**

If the corresponding file is not found, the GSQL Primary server will use the default file in the package. These default files are at:

```text
$(gadmin config get System.AppRoot)/dev/gdk/gsql/src/TokenBank/TokenBank.cpp
$(gadmin config get System.AppRoot)/dev/gdk/gsql/src/QueryUdf/ExprUtil.hpp
$(gadmin config get System.AppRoot)/dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp
```

### **File Path Configuration**

In Pre-3.1 release design, the file path used in loading jobs refers to the file in m1, unless the user specifies machine name before the path \(ALL, ANY, m1, m2,…\). In the new HA design, the Primary server can be running on any machine, and can be switched. This means GSQL server may or may not find the file. To be back-compatible we prefix a machine name if the client is in TigerGraph cluster.

Users can specify the node ID before the path using: ALL, ANY, m1, m2 and so forth. Declaring ALL or ANY as host ID will load files from every cluster node.

User can use form like “m1\|m3\|m4” to declare the combination of several nodes.

If the hosts are not specified, it will look for the host ID of the current node that is running the loading job, \(through searching the nodes in $\(gadmin config get GSQL.BasicConfig.Nodes\)\). If not found, it will use node “m1” by default.

```text
# current refers to /path/to/csv in m1
LOAD "/path/to/csv" TO VERTEX vt VALUES($0)
LOAD "ALL:/path/to/csv" TO VERTEX vt VALUES($0)
LOAD "m1|m2:/path/to/csv" TO VERTEX vt VALUES($0)
```

Data source can be created and used with a file path or a JSON string, same as above.

```text
create data_source kafka k1 for graph poc_graph
set k1 = "/tmp/kafka_config.json"
create data_source kafka k2 = "/tmp/kafka_config.json"

CREATE LOADING JOB load_kafka FOR GRAPH poc_graph {
  DEFINE FILENAME f1 = "$k1:/tmp/topic_partition_config.json";
  LOAD f1
      TO VERTEX MyNode VALUES ($2)
      USING SEPARATOR="|";
}
```

### **GSQL Client connection setup:**

GSQL client can connect to GSQL server in the different ways with the following priority order:

#### **Using IP address:**

Users can specify the ip and port when calling GSQL client using “gsql -i” or “gsql -ip”. For example:

```text
gsql -ip 192.168.11.32:14240,192.168.11.34:14240,192.168.11.36
```

GSQL clients will try these ips and ports one by one. Notice the port is optional, it will use 14240 by default, which is the default port for GSQL server. 

#### **Using GSQL IP Configuration:**

If “gsql -i” or “gsql -ip” are not used, GSQL client will search the file gsql\_server\_ip\_config where the user runs the GSQL client. The file gsql\_server\_ip\_config should be a one-line file such as shown below. GSQL client will traverse the ips and ports in the file in its order.

```text
172.18.0.101,172.18.0.102:14240,172.18.0.103:14240 
```

Similarly, the port number is also optional, using 14240 by default.

#### **Using default local server:**

If  “gsql -i” or “gsql -ip” are not used, and the file gsql\_server\_ip\_config does not exist where “gsql” is called, GSQL client will try to connect to the local server \(127.0.0.1:8123\).

### **Setting GSQL HA Configuration**

Use gadmin config to get/set the following configurations related to GSQL High Availability.

The first is the heartbeat interval in milliseconds. The second \(“max misses”\) is the total timeout for switching to the Primary server which will measure the number of heartbeat intervals. It must be at least 2 to allow 1 heartbeat miss.

```text
Controller.LeaderElectionHeartBeatIntervalMS = 2000
Controller.LeaderElectionHeartBeatMaxMiss = 4
```

For example, if we use “IntervalMS = 2000” and “max misses = 4” as shown above, then the total timeout is 2s×4 = 8 seconds. So the current Primary server will be switched if its heartbeat has stopped for more than 8 seconds.  
****

