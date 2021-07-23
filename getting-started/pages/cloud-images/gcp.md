# Get Started on Google Cloud

This tutorial will show you how to start TigerGraph from an image on Google Cloud. Please select your edition from below:

## **Deploying Your Instance**‌

1. Go to Google Cloud Marketplace [https://console.cloud.google.com/marketplace](https://console.cloud.google.com/marketplace) and search for  "TigerGraph Enterprise Edition". Choose the latest edition to access the most up-to-date features. 

2. Click on "Launch"​‌.

![](../../../.gitbook/assets/console-page%20%289%29.png)

 3. The default settings are fine for most users, but feel free to modify them. When ready, click on "Deploy". 

**Notes:**   
The instance type needs to have at least 4 CPUs and 16GB RAM for TigerGraph to work properly. 

The "Allow TCP port 14240 traffic from the Internet" checkbox must be checked if you want to access GraphStudio \(TigerGraph's visualization platform\). For more about GraphStudio, see the [GraphStudio UI Guide](../../../ui/graphstudio/).

For information on how to set up authentication please see [User access management](../../../admin/admin-guide/user-access/).

The "Allow TCP port 9000 traffic from the Internet" checkbox must be checked if you want to send RESTful requests to TigerGraph from outside the instance \(this includes configuring the GSQL client on a remote machine\). For more about the REST API, see the [TigerGraph RESTful API User Guide](../../../dev/restpp-api/).‌

For more about the TigerGraph Platform, see the [TigerGraph Platform Overview](../../../tigergraph-platform-overview/internal-architecture.md).​‌

![](../../../.gitbook/assets/deployment-form%20%289%29.png)

4. That's it! The TigerGraph instance has been successfully deployed on Google Cloud.​‌

![](../../../.gitbook/assets/deploying-page%20%289%29.png)

## **Starting TigerGraph on Your Instance**

‌1. Log on to the instance and switch to user `tigergraph` using the following command:

```text
sudo su - tigergraph
```

![](../../../.gitbook/assets/login-to-tigergraph%20%288%29.png)

2. Run the following command to check the current status of TigerGraph. The services **"ADMIN", "CTRL", "ETCD", "IFM", "KAFKA", and "ZK" are started automatically** and should be up at this point. If any of them are not or you get the following error message, **please wait for 30 to 60 seconds and check the status again** before reporting it to TigerGraph support.

```text
gadmin status
```

![](../../../.gitbook/assets/gadmin-status%20%283%29.png)

![](../../../.gitbook/assets/gadmin-status-error-message%20%283%29.png)

3. Run the following command to start TigerGraph:

```text
gadmin start
```

![](../../../.gitbook/assets/gadmin-start%20%2811%29.png)

4. Check the status again. All services should be up at this point:

```text
gadmin status
```

![](../../../.gitbook/assets/gadmin-status-after-start%20%283%29.png)

5. TigerGraph has been successfully started on your cloud instance.‌

## TigerGraph License on Google Cloud Images

The TigerGraph Enterprise edition image comes with **a perpetual license** that will **only work on the Google Cloud instance it's installed on**. Please run the following command to see it:

```text
gadmin license status
```

![](../../../.gitbook/assets/gadmin-license-status%20%284%29.png)

