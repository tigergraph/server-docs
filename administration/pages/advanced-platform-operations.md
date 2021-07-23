# Advanced Platform-layer Commands

This page documents a list of advanced Linux commands that simplify platform operations that are performed often during debugging, especially on high availability \(HA\) clusters. Only the TigerGraph platform owner - the Linux user created during installation has access to the commands on this page.  

{% hint style="info" %}
Users are advised to use these commands only at the guidance and recommendation of TigerGraph support.  
{% endhint %}

## Connection between nodes

### Connect to another node via SSH

```text
$ gssh <node_name>
```

This command allows you to connect to another node in your cluster via SSH. 

#### Example:

```bash
# Originally on m1
[tigergraph@ip-172-31-88-111 ~]$ gssh m3
Last login: Fri Apr 23 18:24:27 2021
# Now connected to m3 via ssh
[[tigergraph@ip-172-31-93-187 ~]$ 
```

## Loading data

### Offline loading

```bash
$ gautoloading.sh (-g <graph_name> -j <loading_job_name> | path_to_config_file)
```

With huge data volumes, data loading can be time-consuming. If you find yourself often loading huge volumes of data into an empty graph, and your data volume is so large that your loading jobs are taking hours to complete, you might consider using offline loading to speed up data loading. 

In order to use offline loading, all the filename variables in the loading job must take an initial path value. After creating the loading job and ensuring that all the data files are referenced correctly in the loading job, use the options `-g` and `-j` to specify the graph and loading job to run. During offline loading, your database is focused on loading data and will not be able to handle requests and queries.

{% hint style="danger" %}
Offline loading deletes all existing graph data before it starts. Back up your data before using offline loading. 
{% endhint %}

#### Options

* `-g <graph_name>`: Name of the graph whose loading job to run
* `-j <loading_job_name>`: Name of the loading job to run 

#### Example

The following command runs the loading job `load_ldbc_snb` on the graph `ldbc_snb`:

```bash
$ gautoloading.sh -g ldbc_snb -j load_ldbc_snb
```

You can also provide the graph name and the loading job name with a config file written in Bash:

{% code title="~/example\_config" %}
```bash
# the name of the graph for the initial loading
GRAPH_NAME="tpc_graph"

# the name of loading jobs separated by white space
LOADING_JOBS=("load_test")
```
{% endcode %}

Once you have the config file, you can run `gautoloading.sh` with the config file instead of the `-g` and `-j` options:

```bash
$ gautoloading.sh ~/example_config
```

## File operations

### Copy files on the specified nodes

```bash
$ gscp <all|component_name|node_list> <source_path> <target_dir>
```

This command allows you to copy files from the current node to target folders on multiple nodes at the same time. The file or directory on the current node specified by the source path will be copied into the target folder on every node. If the target folder does not exist at the path given, the target folder will be created automatically. You can also specify multiple source files or directories, in which case, the source paths need to be absolute paths, put in quotes, and separated by space. 

You can specify the nodes where you want the copy operation to occur in the following ways:

* `gscp all <source_path> <target_dir>` will execute the command on all nodes
* `gscp <component_name> <source_path> <target_dir>` will execute the command on nodes where the component you specified is running
* `gscp <node_list> <source_path> <target_dir>` will execute the command on the nodes you specify in the node list

#### Example

{% tabs %}
{% tab title="Single source" %}
```cpp
$ gscp all /tmp/gscp_test /tmp/gscp_test_folder

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.88.179 ...

### Connecting to remote server 172.31.91.208 ...

// A copy of gscp_test is on every node
$ grun all 'ls /tmp/gscp_text_folder'

### Connecting to local  server 172.31.91.54 ...
gscp_test

### Connecting to remote server 172.31.88.179 ...
gscp_test

### Connecting to remote server 172.31.91.208 ...
gscp_test

// Copy file to the target folder only on nodes where GPE is running
$ gscp gpe /tmp/gscp_test1 /tmp/gscp_test_folder

// Copy file to a specified list of nodes
$ gscp m1,m2 /tmp/gscp_test3 /tmp/gscp_test_folder
```
{% endtab %}

{% tab title="Multiple sources" %}
```cpp
$ gscp all "/tmp/gscp_test1 /tmp/gscp_test2" /tmp/gscp_test_folder

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.88.179 ...

### Connecting to remote server 172.31.91.208 ...

// Copies of both files are on every node
$ grun all 'ls /tmp/gscp_text_folder'

### Connecting to local  server 172.31.91.54 ...
gscp_test1 gscp_test2

### Connecting to remote server 172.31.88.179 ...
gscp_test1 gscp_test2

### Connecting to remote server 172.31.91.208 ...
gscp_test1 gscp_test2
```
{% endtab %}
{% endtabs %}

### Download file from another node

```bash
$ gfetch <all|component_name|node_list> <source_path> <target_dir>
```

This command downloads a file or directory from every specified node to the target directory on the current node. 

#### Example

```cpp
$ gfetch all ~/test.txt ~/test_folder

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.88.179 ...

### Connecting to remote server 172.31.91.208 ...
scp: /home/tigergraph/test.txt: No such file or directory

// Nothing is downloaded if the file does not exist on a node
$ ls ~/test_folder
test.txt_m1  test.txt_m2  
```

## Run commands on multiple nodes

### Run commands sequentially

```bash
$ grun <all|component_name|node_list> '<command>'
```

This command allows you to run commands on a specified list of nodes in your cluster one by one, and the output from every node will be visible to the terminal. `grun` will wait for the command to finish running on one node before executing the command on the next node.

You can specify which nodes to run commands on in the following ways:

* `grun all '<command>'` will execute the command on all nodes
* `grun <component_name> '<command>'` will execute the command on nodes where the component you specified is running
* `grun <node_list> '<command>'` will execute the commands on the nodes you specify in the node list

#### Example

{% tabs %}
{% tab title="All nodes" %}
```bash
grun all 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...
hello world

### Connecting to remote server 172.31.88.179 ...
hello world

### Connecting to remote server 172.31.91.208 ...
hello world
```
{% endtab %}

{% tab title="By component name" %}
```bash
# Run 'echo "hello world"' on every node where GPE is running
grun gpe 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...
hello world

### Connecting to remote server 172.31.88.179 ...
hello world

### Connecting to remote server 172.31.91.208 ...
hello world
```
{% endtab %}

{% tab title="By node list" %}
```bash
grun m1,m3 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...
hello world

### Connecting to remote server 172.31.91.208 ...
hello world
```
{% endtab %}
{% endtabs %}

### Run commands in parallel

```bash
$ grun_p <all|component_name|node_list> '<command>'
```

This command allows you to run commands on a specified list of nodes in your cluster in parallel, and the output will be visible to the terminal where the `grun_p` command was run. You can specify the nodes to run commands on in the following ways:

* `grun_p all '<command>'` will execute the command on all nodes
* `grun_p <component_name> '<command>'` will execute the command on nodes where the component you specified is running
* `grun_p <node_list> '<command>'` will execute the commands on the nodes you specify in the node list. The list of nodes should be separated by a comma, e.g.: `m1,m2`

{% tabs %}
{% tab title="All nodes " %}
```aspnet
$ grun_p all 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.88.179 ...

### Connecting to remote server 172.31.91.208 ...

### ---- (m1)_172.31.91.54 ---0--
hello world

### ---- (m2)_172.31.88.179 ---0--
hello world

### ---- (m3)_172.31.91.208 ---0--
hello world
```
{% endtab %}

{% tab title="By component" %}
```
$ grun_p gpe 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.88.179 ...

### Connecting to remote server 172.31.91.208 ...

### ---- (m1)_172.31.91.54 ---0--
hello world

### ---- (m2)_172.31.88.179 ---0--
hello world

### ---- (m3)_172.31.91.208 ---0--
hello world
```
{% endtab %}

{% tab title="By node list" %}
```
$ grun_p m1,m3 'echo "hello world"'

### Connecting to local  server 172.31.91.54 ...

### Connecting to remote server 172.31.91.208 ...

### ---- (m1)_172.31.91.54 ---0--
hello world

### ---- (m3)_172.31.91.208 ---0--
hello world
```
{% endtab %}
{% endtabs %}

## Display cluster information

### Show current node IP

```bash
$ gmyip
```

This command returns the private IP address of your current node. 

#### Example:

```bash
$ gmyip
172.31.93.187 # Current node IP address 
```

### Show current node number and servers

```bash
$ ghostname
```

This command returns your current node number as well as all servers that are running on the current node. 

#### Example

In this example, `m1` is the current node number, and `ADMIN#1`, `admin#1` etc. are all servers that are running on `m1`.

```cpp
$ ghostname

m1 ADMIN#1 admin#1 CTRL#1 ctrl#1 DICT#1 dict#1 ETCD#1 etcd#1 EXE_1 exe_1 GPE_1#1 gpe_1#1 GSE_1#1 gse_1#1 GSQL#1 gsql#1 GUI#1 gui#1 IFM#1 ifm#1 KAFKA#1 kafka#1 KAFKACONN#1 kafkaconn#1 KAFKASTRM-LL_1 kafkastrm-ll_1 NGINX#1 nginx#1 RESTPP#1 restpp#1 TS3_1 ts3_1 TS3SERV#1 ts3serv#1 ZK#1 zk#1
```

### Show deployment information

```bash
$ gssh
```

The `gssh` command, when used without arguments, outputs information about server deployments in your cluster. The output contains the names and IP addresses of every node. For each node, the output shows the full list of servers that are running on the node. For each server, the output shows the full list of the nodes that the server is running on. 

#### Example

```aspnet
$ gssh

Usage: gssh m1|gpe_1#1|gse1_1#1|...
Usage: ----------------Available hosts--------------
Host *
    IdentityFile /home/tigergraph/.ssh/tigergraph_rsa
    Port 22

Host m1 ADMIN#1 admin#1 CTRL#1 ctrl#1 DICT#1 dict#1 ETCD#1 etcd#1 EXE_1 exe_1 GPE_1#1 gpe_1#1 GSE_1#1 gse_1#1 GSQL#1 gsql#1 GUI#1 gui#1 IFM#1 ifm#1 KAFKA#1 kafka#1 KAFKACONN#1 kafkaconn#1 KAFKASTRM-LL_1 kafkastrm-ll_1 NGINX#1 nginx#1 RESTPP#1 restpp#1 TS3_1 ts3_1 TS3SERV#1 ts3serv#1 ZK#1 zk#1
    HostName 172.31.91.54

Host m2 ADMIN#2 admin#2 CTRL#2 ctrl#2 DICT#2 dict#2 ETCD#2 etcd#2 EXE_2 exe_2 GPE_2#1 gpe_2#1 GSE_2#1 gse_2#1 GSQL#2 gsql#2 GUI#2 gui#2 IFM#2 ifm#2 KAFKA#2 kafka#2 KAFKACONN#2 kafkaconn#2 KAFKASTRM-LL_2 kafkastrm-ll_2 NGINX#2 nginx#2 RESTPP#2 restpp#2 TS3_2 ts3_2 ZK#2 zk#2
    HostName 172.31.88.179

Host m3 ADMIN#3 admin#3 CTRL#3 ctrl#3 DICT#3 dict#3 ETCD#3 etcd#3 EXE_3 exe_3 GPE_3#1 gpe_3#1 GSE_3#1 gse_3#1 GSQL#3 gsql#3 GUI#3 gui#3 IFM#3 ifm#3 KAFKA#3 kafka#3 KAFKACONN#3 kafkaconn#3 KAFKASTRM-LL_3 kafkastrm-ll_3 NGINX#3 nginx#3 RESTPP#3 restpp#3 TS3_3 ts3_3 ZK#3 zk#3
    HostName 172.31.91.208

#cluster.nodes: m1:172.31.91.54,m2:172.31.88.179,m3:172.31.91.208
#admin.servers: m1,m2,m3
#ctrl.servers: m1,m2,m3
#dict.servers: m1,m2,m3
#etcd.servers: m1,m2,m3
#exe.servers: m1,m2,m3
#gpe.servers: m1,m2,m3
#gse.servers: m1,m2,m3
#gsql.servers: m1,m2,m3
#gui.servers: m1,m2,m3
#ifm.servers: m1,m2,m3
#kafka.servers: m1,m2,m3
#kafkaconn.servers: m1,m2,m3
#kafkastrm-ll.servers: m1,m2,m3
#nginx.servers: m1,m2,m3
#restpp.servers: m1,m2,m3
#ts3.servers: m1,m2,m3
#ts3serv.servers: m1
#zk.servers: m1,m2,m3
#log.root: /home/tigergraph/tigergraph/log
#app.root: /home/tigergraph/tigergraph/app/3.1.1
#data.root: /home/tigergraph/tigergraph/data
```

### Show graph status

```text
$ gstatusgraph
```

This command returns the size of your data, the number of existing vertices and edges, as well as the number of deleted and skipped vertices on every node in your cluster. If you are running TigerGraph on a single node, it will return the same information that one node. 

#### Single-node example

```bash
$ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 437MiB, IDS size: 103MiB, Vertex count: 3181724, Edge count: 34512076, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
```

#### Cluster example

```bash
$ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 246MiB, IDS size: 31MiB, Vertex count: 1152822, Edge count: 10908545, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[m2     ] Partition size: 248MiB, IDS size: 31MiB, Vertex count: 1157325, Edge count: 11004342, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[m3     ] Partition size: 225MiB, IDS size: 29MiB, Vertex count: 1049883, Edge count: 10009479, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
```

