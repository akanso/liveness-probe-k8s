
# Image URL to use all building/pushing image targets

IMG ?=python-liveness:1.0

# Run against the configured Kubernetes cluster in ~/.kube/config
run:
	dotnet run

# Build the docker image
docker-build:
	docker build . -t ${IMG}

# Push the docker image
docker-push:
	docker push ${IMG}


# deploy to k8s
deploy: docker-build
	kubectl apply -f ./

# clean up k8s created objects
cleanup:
	kubectl delete -f  ./
	docker rmi -f ${IMG}
