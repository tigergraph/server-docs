# Get Started with Docker

This document provides step-by-step instructions on how to pull the latest TigerGraph Enterprise Edition docker image to your host machine. You can follow the sections in sequence to set up the TigerGraph docker environment.

The latest TigerGraph docker image includes the following content:

* The latest version of TigerGraph
* Linux packages:
  * openssh-server
  * git
  * wget
  * curl
  * emac
  * vim
  * jq
  * tar
* Tutorial material
  * GSQL 101
  * GSQL 102
* The latest GSQL open-source graph algorithm library

This follow-along video shows the whole setup process: [https://www.youtube.com/watch?v=V5VvgJyjLxA](https://www.youtube.com/watch?v=V5VvgJyjLxA)

## 1. Install Docker Desktop

Follow the steps below to install Docker Desktop on your machine and configure it with sufficient resources for TigerGraph:

1. Install Docker on your OS:
   * To install Docker for Mac OS, follow this video: [https://www.youtube.com/watch?v=MU8HUVlJTEY](https://www.youtube.com/watch?v=MU8HUVlJTEY)
   * To install Docker for Linux, follow these instructions:
     * Centos: [https://docs.docker.com/install/linux/docker-ce/centos/](https://docs.docker.com/install/linux/docker-ce/centos/)
     * Ubuntu: [https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
   * To install Docker for Windows OS, follow this video: [https://www.youtube.com/watch?v=ymlWt1MqURY](https://www.youtube.com/watch?v=ymlWt1MqURY)
2. Configure Docker Desktop with sufficient resources: 
   * Recommended: 4 cores and 16GB memory 
   * Minimum: 2 cores and 10GB memory
   * Click the Docker Desktop icon, click **Preferences** &gt;&gt; **Resources**, drag the CPU and Memory sliders to the desired configuration, save and restart Docker Desktop

## 2. Prepare a Shared Folder on Host OS to be shared with Docker Container

Open a shell on your host machine and create or select a directory for sharing data between your host machine and docker container. Grant read+write+execute permission to the folder. For example, to create a folder called data in Linux:

```text
    $ mkdir data
    $ chmod 777 data
```

You can mount \(map\) the data folder to a folder under the docker container, which allows you to share files between your host OS and Docker OS. 

For example, if you mount the host OS folder `~/data` to the docker folder `/home/tigergraph/mydata`,  then anything you put on `~/data` will be visible in the docker container under `/home/tigergraph/mydata`, and vice versa.

## 3. Run TigerGraph Docker image as a daemon

Run the following command to pull the TigerGraph docker image, bind ports, map a shared data folder, and start a container from the image. Note: this command is very long; please make sure you copy the whole command by dragging the scroll bar to the end:

```text
$ docker run -d -p 14022:22 -p 9000:9000 -p 14240:14240 --name tigergraph --ulimit nofile=1000000:1000000 -v ~/data:/home/tigergraph/mydata -t docker.tigergraph.com/tigergraph:latest
```

* Here is a breakdown of the options and arguments in the command:
  * `-d`: make the container run in the background.
  * `-p`: map docker 22 port to host OS 14022 port, 9000 port to host OS 9000 port, 14240 port to host OS 14240 port.
  * `--name`: name the container tigergraph.
  * `--ulimit`: set the `ulimit` \(the number of open file descriptors per process\) to 1 million.
  * `-v`: mount the host OS `~/data` folder to the docker `/home/tigergraph/mydata` folder using the -v option. If you are using Windows, change the above ~/data to something using windows file system convention, e.g. `c:\data`
  * `-t`: allocate a pseudo-TTY
  * `docker.tigergraph.com/tigergraph:latest`:  download the latest docker image from the TigerGraph docker registry URL docker.tigergraph.com/tigergraph.

{% hint style="info" %}
Replace "latest" with a specific version number if a dedicated version of TigerGraph is to be used. E.g., if you want to get the 3.0.5 version, the URL should be:

`docker.tigergraph.com/tigergraph:3.0.5` 

To use the legacy developer editions, use:

`docker.tigergraph.com/tigergraph-dev`
{% endhint %}

If you use Windows and have disk drive permission issues with the above command,  try the following command instead \(this command does not map the shared folder on your host machine to your container\) :

```text
$ docker run -d -p 14022:22 -p 9000:9000 -p 14240:14240 --name tigergraph --ulimit nofile=1000000:1000000 -t docker.tigergraph.com/tigergraph:latest
```

## 4. Use SSH to connect to your container

After launching the container, you can use SSH to connect to your container:

1. Verify that the container is running. You should see a row that describes the running container after running the command below:

   ```text
   $ docker ps | grep tigergraph
   ```

2. Use ssh to open a shell to the container. At the prompt, enter `tigergraph`  as the password. Note that we have mapped the host 14022 port to the container's 22 port \(the ssh default port\), so on the host we use ssh to connect to port 14022. 

   ```text
   $ ssh -p 14022 tigergraph@localhost
   ```

## 5. Start TigerGraph

1. After connecting to the container via ssh, inside the container, start all TigerGraph services with the following command \(which may take up to one minute\):

   ```text
   $ gadmin start all
   ```

2. Run the `gsql` command as shown below to start the GSQL shell. If you are new to TigerGraph, you can run the [GSQL 101](../gsql-101/) tutorial now.

   ```text
   $ gsql
   GSQL > 
   ```

3. Start GraphStudio, TigerGraph's visual IDE, by visiting `http://localhost:14240`

   in a browser on your laptop \(host OS\).

## Operation Commands Cheat Sheet

* After you start Docker Desktop, use the commands below to stop and restart the container:

  ```text
    $ docker container stop tigergraph
    $ docker container start tigergraph
  ```

* Start the TigerGraph service within the container:

  ```text
    $ gadmin start all
    $ gadmin stop  all
  ```

* ssh to the container. Note: if localhost is not recognized, remove the localhost entry from ~/.ssh/known\_hosts

  ```text
    $ sed -i.bak '/localhost/d' ~/.ssh/known_hosts
    $ ssh -p 14022 tigergraph@localhost
  ```

  > Linux users can access the container through its ip address directly:

  ```text
    $ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tigergraph
    $vssh tigergraph@<container_ip_address>
  ```

* Default user: `tigergraph`
* Default password: `tigergraph`
* After running `gadmin start`, you can go to GraphStudio. Open a browser on your laptop \(host OS\) and access GraphStudio at the following URL:

  ```text
    http://localhost:14240
  ```

* Check the version of GSQL:

  ```text
  $ gsql version
  ```

