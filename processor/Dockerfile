# Pulling ubuntu from dockerhub
FROM ubuntu:22.04

ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Sync repositories
RUN apt update -y

# Install Git
RUN apt install -y git

# Install Java and Maven
RUN apt install -y openjdk-17-jdk maven

# Go to CK folder to work
WORKDIR /usr/share/lab01

# Clone CK
RUN git clone https://github.com/mauricioaniche/ck.git .

# Build CK
RUN mvn clean compile package

# Install Python3
RUN apt install -y python3 python3-pip

# Go to script folder to work
WORKDIR /usr/share/scriptlab

# Copy files to container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Define script as entrypoint of container
ENTRYPOINT ["python3", "/usr/share/scriptlab/script.py"]