# Get Started on AWS

This tutorial will show you how to start TigerGraph Enterprise Edition from an image on AWS.

## **Deploying Your Instance**

1. Go to [AWS Marketplace](https://aws.amazon.com/marketplace/) and search for TigerGraph.  
  
2. Click "Continue to Subscribe".

![Subscribe Page](../../../.gitbook/assets/subscribe-page%20%281%29.png)

3. Click on "Continue to Configuration".

![Pre Configuration Page](../../../.gitbook/assets/go-to-config-page%20%281%29.png)

  
4. Select the Software Version and Region. We recommend selecting the latest version for the most up-to-date features. After making your selections, click on "Continue to Launch".

![Configuration Page](../../../.gitbook/assets/configuration-page%20%281%29.png)

5. Select the instance type, security group settings, and other settings. The default settings are fine for most users, but feel free to modify them. Click "Launch" when finished.  
  
**Notes:**   
The instance type needs to have at least 4 CPUs and 16GB RAM for TigerGraph to work properly.  
  
The security group must allow inbound TCP traffic to port 14240 if you want to access GraphStudio \(TigerGraph's visualization platform\). For more about GraphStudio, see the [GraphStudio UI Guide](../../../ui/graphstudio/).  
  
The security group must allow inbound TCP traffic to port 9000 if you want to send RESTful requests to TigerGraph from outside the instance \(this includes configuring the GSQL client on a remote machine\). For more about the REST API, see the [TigerGraph RESTful API User Guide](../../../dev/restpp-api/).

For more about the TigerGraph Platform, see the [TigerGraph Platform Overview](../../../tigergraph-platform-overview/internal-architecture.md).

![Configuration Page 2](../../../.gitbook/assets/configuration-page-2%20%281%29.png)

6. That's it!  The TigerGraph instance has been successfully deployed on AWS.

![Deploying Page](../../../.gitbook/assets/launch-successful%20%281%29.png)

## **Starting TigerGraph on Your Instance**

1. Log on to the instance and switch to user `tigergraph` using the following command:

```bash
sudo su - tigergraph
```

![TigerGraph Login](../../../.gitbook/assets/login-to-tigergraph-user%20%282%29.png)

2. Run the following command to check the current status of TigerGraph. The services **"ADMIN", "CTRL", "ETCD", "IFM", "KAFKA", and "ZK" are started automatically** and should be up at this point. If any of them are not or you get the following error message, **please wait for 30 to 60 seconds and check the status again** before reporting it to TigerGraph support.

```text
gadmin status
```

![Output of gadmin status](../../../.gitbook/assets/gadmin-status%20%282%29.png)

![Gadmin status error message](../../../.gitbook/assets/gadmin-status-error-message%20%282%29.png)

3. Run the following command to start TigerGraph:

```text
gadmin start
```

![Output of gadmin start](../../../.gitbook/assets/gadmin-start%20%2810%29.png)

4. Check the status again. All services should be up at this point:

```text
gadmin status
```

![Gadmin status after running gadmin start](../../../.gitbook/assets/gadmin-status-after-start%20%282%29.png)

5. TigerGraph has been successfully started on your cloud instance.

## TigerGraph License on **AWS** Images

The TigerGraph Enterprise edition image comes with **a perpetual license** that will **only work on the AWS instance it's installed on**. Please run the following command to see it:

```text
gadmin license status
```

![Gadmin license status output](../../../.gitbook/assets/gadmin-license-status%20%283%29.png)

