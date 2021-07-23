# Run Built-in Queries

You now have a graph with data!  You can run some  queries using the built-in REST endpoint calls. 

## Get Vertex/Edge Statistics

Below we call two functions, stat\_vertex\_number and stat\_edge\_number to return the cardinality of each vertex and edge type. 

{% hint style="info" %}
REST endpoints return results in JSON format. JSON data are used for various purposes. But JSON data can’t be read easily from JSON file by using bash script like other normal files. **jq** tool is used to solve this problem

We recommend you install jq and redirect the REST call result to jq before it is output.  
{% endhint %}

{% code title="Linux Shell" %}
```sql
#get vertex cardinality
curl -X POST 'http://localhost:9000/builtins/social' -d  '{"function":"stat_vertex_number","type":"*"}'  | jq .
```
{% endcode %}

```sql
#results
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "v_type": "person",
      "count": 7
    }
  ]
}
```

{% code title="Linux Shell" %}
```sql
#get edge cardinality
curl -X POST 'http://localhost:9000/builtins/social' -d  '{"function":"stat_edge_number","type":"*"}' | jq .
```
{% endcode %}

```sql
#results
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "friendship",
      "count": 7
    }
  ]
}
```

## Select Vertices

If you want to lookup the details about a vertex with its primary\_id, you can use the following REST call.

{% code title="Linux Shell" %}
```sql
curl -X GET "http://localhost:9000/graph/{graph_name}/vertices/{vertex_type}/{vertex_id}"
```
{% endcode %}

**Example**. Find a person vertex whose primary\_id is "Tom".

{% code title="Linux Shell" %}
```sql
 curl -X GET "http://localhost:9000/graph/social/vertices/person/Tom" | jq .
```
{% endcode %}

```sql
 #result
 {
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "v_id": "Tom",
      "v_type": "person",
      "attributes": {
        "name": "Tom",
        "age": 40,
        "gender": "male",
        "state": "ca"
      }
    }
  ]
}
```

## Select Edges

In similar fashion, we can see details about edges.  To describe an edge, you name the types of vertices and edges in the two parts or three parts of a URL.

{% code title="Linux Shell" %}
```sql
#two parts
curl -X GET "http://localhost:9000/graph/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/"

#three parts
curl -X GET "http://localhost:9000/graph/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/{target_vertex_type}/{target_vertex_id}"
```
{% endcode %}

**Example**. Find all friendship edges whose source vertex's primary\_id is "Tom".

{% code title="Linux Shell" %}
```sql
curl -X GET "http://localhost:9000/graph/social/edges/person/Tom/friendship/" | jq .
```
{% endcode %}

```sql
#result
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "friendship",
      "directed": false,
      "from_id": "Tom",
      "from_type": "person",
      "to_id": "Dan",
      "to_type": "person",
      "attributes": {
        "connect_day": "2017-06-03 00:00:00"
      }
    },
    {
      "e_type": "friendship",
      "directed": false,
      "from_id": "Tom",
      "from_type": "person",
      "to_id": "Jenny",
      "to_type": "person",
      "attributes": {
        "connect_day": "2015-01-01 00:00:00"
      }
    }
  ]
}
```

For more built-in REST endpoints, you can refer to[ ](../../dev/restpp-api/built-in-endpoints.md)the [Built-in Endpoints page](../../dev/restpp-api/built-in-endpoints.md).

