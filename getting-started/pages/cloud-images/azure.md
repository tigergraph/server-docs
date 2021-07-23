# Get Started on Microsoft Azure

This tutorial will show you how to start TigerGraph Enterprise Edition from an image on Microsoft Azure.

## **Deploying Your Instance**

1. Go to [Microsoft Azure Marketplace](%20https://portal.azure.com/#blade/Microsoft_Azure_Marketplace/MarketplaceOffersBlade/selectedMenuItemId/home) and search for "TigerGraph".  
  
2. Select your software plan and Click "Create". Select the latest plan \(with the highest version number\) to access the latest features.

![Create Page](../../../.gitbook/assets/create-page%20%281%29.png)

3. Fill out the "Resource group", "Virtual machine name", "Username" and "SSH Public key" fields. The default values should work for the rest of the fields. Then click "**Next: Disks &gt;**".

![Basic Settings Page](../../../.gitbook/assets/basic-settings-page%20%281%29.png)

4. Keep the default values for all other settings and click "Next" until you see the "Review + Create" page below. Check all your settings and click "Create" when you are satisfied.  
  
**Notes:**   
The instance type needs to have at least 4 CPUs and 16GB RAM for TigerGraph to work properly.  
  
The "NIC network security group" must allow inbound TCP traffic to port 14240 if you want to access GraphStudio \(TigerGraph's visualization platform\). For more about GraphStudio, see the [GraphStudio UI Guide](../../../ui/graphstudio/).  
  
The "NIC network security group" must allow inbound TCP traffic to port 9000 if you want to send RESTful requests to TigerGraph from outside the instance \(this includes configuring the GSQL client on a remote machine\). For more about the REST API, see the [TigerGraph RESTful API User Guide](../../../dev/restpp-api/).

For more about the TigerGraph Platform, see the [TigerGraph Platform Overview](../../../tigergraph-platform-overview/internal-architecture.md).

![Review Page](../../../.gitbook/assets/review-page%20%281%29.png)

5. That's it!  The TigerGraph instance has been successfully deployed on Microsoft Azure.

![Deploying Page](../../../.gitbook/assets/deployment-successful-page%20%281%29.png)

## **Starting TigerGraph on Your Instance**

1. Log on to the instance and switch to user `tigergraph` using the following command:

```bash
sudo su - tigergraph
```

![TigerGraph Login](../../../.gitbook/assets/login-to-tigergraph%20%287%29.png)

2. Run the following command to check the current status of TigerGraph. The services **"ADMIN", "CTRL", "ETCD", "IFM", "KAFKA", and "ZK" are started automatically** and should be up at this point. If any of them are not or you get the following error message, **please wait for 30 to 60 seconds and check the status again** before reporting it to TigerGraph support.

```text
gadmin status
```

![Output of gadmin status](../../../.gitbook/assets/gadmin-status%20%281%29.png)

![Gadmin status error message](../../../.gitbook/assets/gadmin-status-error-message%20%281%29.png)

3. Run the following command to start TigerGraph:

```text
gadmin start
```

![Output of gadmin status](../../../.gitbook/assets/gadmin-start%20%289%29.png)

4. Check the status again. All services should be up at this point:

```text
gadmin status
```

![Gadmin status after running gadmin start](../../../.gitbook/assets/gadmin-status-after-start%20%281%29.png)

5. TigerGraph has been successfully started on your cloud instance.

## TigerGraph License on **Microsoft Azure** Images

The TigerGraph Enterprise edition image comes with **a perpetual license** that will **only work on the Microsoft Azure instance it's installed on**. Please run the following command to see it:

```text
gadmin license status
```

![Gadmin license status output](../../../.gitbook/assets/gadmin-license-status%20%282%29.png)



