# NAGIM clinical data sharing

Scripts and software for pilot of NAGIM clinical data sharing.

## `variant-counts`

Variants counts is a project to produce aggregate variant data across
labs.

We start in the `variant-counts` folder. As a pre-requisite we must
have

* Python
* uv
* Docker
* Homo sapiens vep_data (in a folder called `vep_data` in `variant-counts`)

To run

```shell
uv run -m aggregator.aggregate_with_vep
```

If the Docker client immediately fails - then for some reason Docker is not able to establish
a connection to its server. This seems to be happening on some modern Macs - where it
can't use the default unix socket.

Try (something like)

```
export DOCKER_HOST=unix:///Users/  your username  /.docker/run/docker.sock
```
