# Overview

This repo show a simple example of using Kubernetes liveness probes with a Python example


# Getting started:

## Build the docker image

From the directory where the `Dockerfile exist`, run:

```
 docker build -t python-liveness:1.0 .
```

## Create the pod

From the directory where the `liveness-pod.yaml` exist, run:

```
kubectl create -f './liveness-pod.yaml'
```

# Monitoring:

Once a 500 HTTP status is received, the liveness probe fails

```
kubectl -n default logs test -f
```
```
172.16.6.5 - - [13/Jan/2022 21:00:39] "GET / HTTP/1.1" 200 -
172.16.6.5 - - [13/Jan/2022 21:00:54] "GET / HTTP/1.1" 200 -
172.16.6.5 - - [13/Jan/2022 21:01:09] "GET / HTTP/1.1" 200 -
172.16.6.5 - - [13/Jan/2022 21:01:24] "GET / HTTP/1.1" 500 -
HTTP server started serving at: http://0.0.0.0:8080
Received a SIGTERM signal: 15
Exiting in 3 seconds...
Exiting gracefully
```

Each time the liveness probe fails, K8s (kubelet) will send a sigterm to the container.

```
kubectl -n default get pod test -w
```

```
NAME   READY   STATUS    RESTARTS   AGE
test   1/1     Running   0          5s
test   1/1     Running   1          34s
test   1/1     Running   2          95s
test   1/1     Running   3          110s
test   1/1     Running   4          2m20s
test   0/1     CrashLoopBackOff   4          2m34s
```