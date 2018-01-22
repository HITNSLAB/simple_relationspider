#!/bin/bash
docker login
docker stack deploy --with-registry-auth -c docker-stack.yml sprelaspider
