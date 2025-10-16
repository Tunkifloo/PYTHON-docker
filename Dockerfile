FROM ubuntu:latest
LABEL authors="nicol"

ENTRYPOINT ["top", "-b"]