# Install TigerGraph on Linux

You can install TigerGraph on a Linux machine that meets the [Hardware and Software Requirements](../../admin/admin-guide/hw-and-sw-requirements.md). For a step-by-step guide on installing TigerGraph on your Linux machine, please visit the following page:

{% page-ref page="../../admin/admin-guide/install-and-config/install.md" %}

## Quickstart guide for new users <a id="GETSTARTEDwithTigerGraphv2.1-QuickStartGuideforNewUsers"></a>

### Installation Checklist

1. **CHECK** [Hardware and Software Requirements](../../admin/admin-guide/hw-and-sw-requirements.md)
2. **DOWNLOAD** the TigerGraph platform: [https://info.tigergraph.com/enterprise-free](https://info.tigergraph.com/enterprise-free)
3. **INSTALL** the Platform
   1. For simple single-server installation:   
      Assuming your downloaded file is called &lt;your\_tigergraph\_package&gt;:

      ```bash
      tar xzf <your_tigergraph_package>.tar.gz 
      cd tigergraph*/ 

      # to install license in interactive mode
      sudo ./install.sh

      # to install license in non-interactive mode
      sudo ./install.sh -n
      ```

   2. For additional options, see [TigerGraph Platform Installation Guide](../../admin/admin-guide/install-and-config/install.md)

