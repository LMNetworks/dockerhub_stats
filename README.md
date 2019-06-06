# dockerhub_stats

This is a [Python3](https://www.python.org) tool to fetch repository statistics from [Docker Hub](https://hub.docker.com).

## usage

See definitions for all possible options:

```
$ dockerhub_stats --help
```

Specify a list of one or more repositories and you'll get a nice table with some statistics, you can also specify users/organizations to fetch statistics about all their repositories.
[Docker Official Images](https://docs.docker.com/docker-hub/official_repos/) must be specified as `library/<reponame>` to differentiate them from users and organizations with the same name:

```
$ # a single repo
$ dockerhub_stats lmnetworks/pdns-recursor
+--------------------------+------------------------------------------------------+------------+------------+----------------------------+
| repository name          | description                                          | star count | pull count | last update                |
+--------------------------+------------------------------------------------------+------------+------------+----------------------------+
| lmnetworks/pdns-recursor | PowerDNS Recursor docker image based on Alpine Linux |          1 |    1377873 | 2019-05-23 08:14:23.532358 |
+--------------------------+------------------------------------------------------+------------+------------+----------------------------+

$ # all repos from "alpine" organization
$ dockerhub_stats lmnetworks/pdns-recursor
+--------------------------------+------------------------------------------------------------------------------------+------------+------------+----------------------------+
| repository name                | description                                                                        | star count | pull count | last update                |
+--------------------------------+------------------------------------------------------------------------------------+------------+------------+----------------------------+
| alpine/assume-role             |                                                                                    |          0 |         17 | 2018-11-23 03:52:33.496122 |
| alpine/bombardier              | Auto-trigger docker build for bombardier when new release is announced             |          1 |       7689 | 2019-02-27 10:47:38.545532 |
| alpine/bundle                  | Auto-trigger docker build for bundler when new ruby release is announced           |          0 |       2751 | 2019-04-18 14:49:35.821155 |
| alpine/bundle-terraform-awspec | This is a special version to build a docker image for terraform awspect testing.   |          1 |        125 | 2018-06-24 08:36:33.414454 |
| alpine/flake8                  | Auto-trigger docker build for fake8 via travis ci cronjob                          |          2 |      22980 | 2019-02-26 06:21:04.315627 |
| alpine/git                     | A  simple git container running in alpine linux, especially for tiny linux distro. |         88 |   24319564 | 2019-02-26 05:35:58.779078 |
| alpine/helm                    | Auto-trigger docker build for kubernetes helm when new release is announced        |          7 |     698574 | 2019-06-02 00:57:13.621095 |
| alpine/httpie                  | httpie running in docker alpine (python3+pip3+alpine+httpie)                       |          8 |     891341 | 2017-09-21 12:00:53.517585 |
| alpine/landscape               | Auto-trigger docker build for terraform-landscape when new release is announced    |          1 |        377 | 2019-03-31 05:53:54.652872 |
| alpine/make                    | a simple container to run make command directly                                    |          0 |        223 | 2018-08-01 02:39:41.313208 |
| alpine/node                    |                                                                                    |          0 |       2293 | 2018-05-21 02:26:31.990552 |
| alpine/semver                  | Docker tool for semantic versioning                                                |          0 |       2285 | 2018-08-01 02:39:07.798906 |
| alpine/socat                   | Run socat command in alpine container                                              |         31 |    4407942 | 2018-06-15 00:45:10.867134 |
| alpine/terragrunt              |                                                                                    |          0 |       1065 | 2019-06-05 04:23:00.290400 |
+--------------------------------+------------------------------------------------------------------------------------+------------+------------+----------------------------+

$ # the "alpine" Official Image repository
$ dockerhub_stats library/alpine
+-----------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+
| repository name | description                                                                                       | star count | pull count | last update                |
+-----------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+
| alpine          | A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size! |       5365 | 1336425027 | 2019-05-11 12:41:17.053047 |
+-----------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+

$ # multiple orgs and repos in the same invocation
$ dockerhub_stats lmnetworks library/alpine gitea/gitea gitlab/gitlab-ce gitlab/gitlab-runner
+-----------------------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+
| repository name             | description                                                                                       | star count | pull count | last update                |
+-----------------------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+
| alpine                      | A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size! |       5365 | 1336426370 | 2019-05-11 12:41:17.053047 |
| gitea/gitea                 | Gitea: Git with a cup of tea - A painless self-hosted Git service.                                |        198 |   33646342 | 2019-06-06 06:56:01.724897 |
| gitlab/gitlab-ce            | GitLab Community Edition docker image based on the Omnibus package                                |       2523 |  116657162 | 2019-06-06 03:17:03.955654 |
| gitlab/gitlab-runner        | GitLab CI Multi Runner used to fetch and run pipeline jobs with GitLab CI                         |        511 |  217776740 | 2019-06-05 23:10:10.679837 |
| lmnetworks/alpine           | a basic Alpine Linux image with updates and CA certificates                                       |          0 |         32 | 2019-05-23 07:24:22.727711 |
| lmnetworks/dashing-icinga2  | Docker for Dashing dashboard for Icinga 2 using the REST API                                      |          0 |         28 | 2018-11-22 16:30:27.208300 |
| lmnetworks/new_ssl_detector | Detect and send email if a new ssl cert has been released.                                        |          0 |         26 | 2018-10-01 09:52:23.674498 |
| lmnetworks/pdns-recursor    | PowerDNS Recursor docker image based on Alpine Linux                                              |          1 |    1377873 | 2019-05-23 08:14:23.532358 |
| lmnetworks/python3          | a basic Python3 Docker image                                                                      |          0 |         30 | 2019-05-23 07:31:12.387147 |
| lmnetworks/python3-dev      | Python3 Docker image with development tools                                                       |          1 |         42 | 2019-06-05 10:11:15.678839 |
| lmnetworks/ruby             | a basic Ruby Docker image                                                                         |          0 |         13 | 2019-06-03 09:48:55.622070 |
+-----------------------------+---------------------------------------------------------------------------------------------------+------------+------------+----------------------------+
```

By default tables are sorted alphabetically by repository name, but can be sorted by star count or pull count using the `--sort` option.

### exporting data to InfluxDB

The same data (excluding repository description) can be written to an [InfluxDB]() time series database by specifing the InfluxDB server host:

```
$ # --quiet suppresses standard output
$ dockerhub_stats --quiet --influxdb-host=192.168.100.200 library/influxdb grafana/grafana library/traefik
```

Note that instead of running `dockerhub_stats` multiple times with different repos it is usually better to have a single invocation with the full list of repositories, this way they will be written in InfluxDB with the same timestamp and will be easier / prettier to query and graph.

### running as a Docker image

The entrypoint is already configured to launch `dockerhub_stats` so you just have to provide arguments and parameters.

Getting help:
```
docker run --rm lmnetworks/dockerhub_stats --help
```

Getting a nice table:
```
docker run --rm lmnetworks/dockerhub_stats lmnetworks library/alpine gitea/gitea gitlab/gitlab-ce gitlab/gitlab-runner
```

Writing to InfluxDB and omitting standard output:
```
docker run --rm lmnetworks/dockerhub_stats -q --influxdb-host=192.168.100.200 lmnetworks gitlab library grafana/grafana
```

## building / installing

### runtime reqirements

* [Python](https://www.python.org) >= 3.6
* [PrettyTable](https://pypi.org/project/PrettyTable/) (only when running without `--quiet`)
* [influxdb](https://pypi.org/project/influxdb/) (only when running with `--influxdb-host`)

### manual install from source code

Using [pip](https://pip.pypa.io/en/stable/):

```
$ git checkout https://www.github.com/LMNetworks/docker-dockerhub_stats
$ pip install .
```

Using good old [setuptools](https://pypi.org/project/setuptools/):
```
$ git checkout https://www.github.com/LMNetworks/docker-dockerhub_stats
$ ./setup.py install
```

### Docker image

Automated builds can be found [on Docker Hub](https://hub.docker.com/r/lmnetworks/dockerhub_stats), but if you prefer it is possible to use the `Dockerfile` included with the source code to build an image based on `lmnetworks/python3` ([GitHub](https://www.github.com/LMNetworks/docker-python3), [Docker Hub](https://hub.docker.com/r/lmnetworks/python3)):

```
$ git checkout https://www.github.com/LMNetworks/docker-dockerhub_stats
$ docker build --tag dockerhub_stats .
```

## origin

This tool has been inspired by [Infinity Works Prometheus exporter for the Docker Hub](https://github.com/infinityworks/docker-hub-exporter), go check it out if you need exporting to Prometheus.