# runner
Simple DAG (Directed Acyclic Graph) implementation based on python concurrent.futures

## Installation

### Runner only
1. [Download](https://www.python.org/downloads/) and install Python
2. Install runner
```shell
pip install mltrip-runner
```   
3. Download [JSON]() or [YAML]() DAG example
4. Plot DAG
 ```shell
python -m runner action.json --plot
```   
or
 ```shell
python -m runner action.yml --plot
```  
![action](/examples/json/action.png)
5. Run DAG
 ```shell
python -m runner action.json
```   
or
 ```shell
python -m runner action.yml
```  

### With [runner-hub](https://github.com/PC-Trip/runner-hub)
1. [Download](https://www.python.org/downloads/) and install Python
2. [Download](https://github.com/PC-Trip/runner-hub/archive/refs/heads/main.zip) or clone runner-hub
```shell
git clone https://github.com/PC-Trip/runner-hub.git
```
3. Install some requirements.txt
```shell
cd runner-hub/runner_hub/gmsh
pip install -r requirements.txt
```
4. Plot some DAG
```shell
cd runner-hub/runner_hub/gmsh/tenex/container_simple/dag
python -m runner optimize/optimize.json --plot
```
![action](/examples/dag.png)
5. Run some DAG
```shell
cd runner-hub/runner_hub/gmsh/tenex/container_simple/dag
python -m runner optimize/optimize.json
```
6. See results
```shell
cd runner-hub/runner_hub/gmsh/tenex/container_simple/dag/work
```