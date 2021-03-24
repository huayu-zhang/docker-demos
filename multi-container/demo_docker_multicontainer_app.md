## Multicontainer demo

App
    - python/conda
    - neo4j
    - mysql



## Neo4j

[Neo4j official image](https://hub.docker.com/_/neo4j)

Pull the docker image for neo4j
```shell
docker pull neo4j:4.2.3
```

Create a network for the multicontainer app
```shell
docker network create demo-network
```

Create a docker volume for neo4j data (optionally also conf and logs)
```shell
docker volume create neo4j-data
```

Run the neo4j image with volume binding and network <br>
Publish the port for http and bolt connection <br>
Set initial account and password <br>

```shell
#!/bin/bash

NAME_DATA_VOLUME=neo4j-data
NAME_NEO4J_IMAGE=neo4j:4.2.3
NAME_NEO4J_NETWORK=demo-network
NAME_NETWORK_ALIAS=neo4j

docker run -d \
    --name neo4j-demo \
    --publish 7474:7474 --publish 7687:7687 \
    --network $NAME_NEO4J_NETWORK --network-alias $NAME_NETWORK_ALIAS \
    --volume=$NAME_DATA_VOLUME:/data \
    --env NEO4J_AUTH=neo4j/password \
    $NAME_NEO4J_IMAGE
```

Check the network address
```shell
docker network inspect demo-network
```

### Connect to Neo4j

Via browser [Neo4j](localhost:7474)

To cypher shell
```shell
docker exec -it neo4j-demo cypher-shell -u neo4j -p password
```

To terminal of the container
```shell
docker exec -it neo4j-demo bash
cypher-shell -u neo4j -p password
```

## Mysql

[Mysql official image](https://hub.docker.com/_/mysql/)

### Run sql in a docker container
Pull the docker image for mysql
```shell
docker pull mysql:5.7.33
```

```shell
docker volume create mysql-data
```

```shell
docker run -d \
  --name mysql-demo \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  --network demo-network --network-alias mysql \
  --volume mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:5.7.33
```

### Ways to connect to mysql instance

To sql interface
```shell
docker exec -it mysql-demo mysql --password=my-secret-pw
```

To the terminal
```shell
docker exec -it mysql-demo bash
mysql --password=my-secret-pw
```

Inspect the ip of sql container
```
docker network inspect demo-network
```

## Python/Conda

### Setup conda env

```shell
conda create -y -n multi-container-demo python=3.7
conda activate multi-container-demo
conda install -c anaconda -y mysql-connector-python
conda install -c conda-forge -y neo4j-python-driver
conda env export > environment.yml
```

### The env: environment.yml

```yaml
name: multi-container-demo
channels:
  - anaconda
  - conda-forge
  - defaults
dependencies:
  - _libgcc_mutex=0.1=main
  - ca-certificates=2020.12.5=ha878542_0
  - certifi=2020.12.5=py37h89c1867_1
  - ld_impl_linux-64=2.33.1=h53a641e_7
  - libffi=3.3=he6710b0_2
  - libgcc-ng=9.1.0=hdf63c60_0
  - libprotobuf=3.6.0=hdbcaa40_0
  - libstdcxx-ng=9.1.0=hdf63c60_0
  - mysql-connector-c=6.1.11=h597af5e_1
  - mysql-connector-python=8.0.18=py37h9c95fcb_1
  - ncurses=6.2=he6710b0_1
  - neo4j-python-driver=4.2.1=pyhd8ed1ab_1
  - openssl=1.1.1j=h27cfd23_0
  - pip=21.0.1=py37h06a4308_0
  - protobuf=3.6.0=py37hf484d3e_0
  - python=3.7.10=hdb3f193_0
  - python_abi=3.7=1_cp37m
  - pytz=2021.1=pyhd8ed1ab_0
  - readline=8.1=h27cfd23_0
  - setuptools=52.0.0=py37h06a4308_0
  - six=1.15.0=py_0
  - sqlite=3.35.2=hdfb4753_0
  - tk=8.6.10=hbc83047_0
  - wheel=0.36.2=pyhd3eb1b0_0
  - xz=5.2.5=h7b6447c_0
  - zlib=1.2.11=h7b6447c_3
prefix: /home/huayu/anaconda3/envs/multi-container-demo
```

### The Dockerfile for buiding the python script

```Dockerfile
FROM continuumio/miniconda3

COPY . /home

RUN cd /home \
  && ENV_NAME=$(cat environment.yml | grep name | cut -c7-) \
  && conda env create -f environment.yml \
  && echo "source activate "$ENV_NAME > ~/.bashrc \
  && apt install nano

ENV PATH /opt/conda/envs/env/bin:$PATH

CMD ["/bin/bash"]
```

#### Build the image

```shell
docker build -t multi-container-demo:0.0.0 -f Dockerfile_conda_py .
```
Run the image with network connection
```shell
docker run -itd \
   --name pysrc \
   --network demo-network \
   multi-container-demo:0.0.0
```

Connect to the docker container
```shell
docker exec -it pysrc bash
```

