
#!/bin/bash
echo "This script may possibly need restart the system"
echo "Please rerun this script after a potential restart to finish deployment"
FILE=./linux.zip
RUNTIME=$(grep -oP '(?<=RUNTIME=).*' .prod.env)
if [ ! -f "$FILE" ]; then
  sudo apt install curl
  sudo apt install unzip
  curl -L https://github.com/amboltio/emily-cli/releases/download/Release-v1.2.0/linux.zip -O
  unzip linux.zip
  if [ "$RUNTIME" = "nvidia" ]; then
    ./linux/emily doctor --silent --fix docker docker-compose nvidia-docker nvidia-driver
  else
    ./linux/emily doctor --silent --fix docker docker-compose
  fi
fi
rm -f linux.zip
rm -rf linux

FILE_PATH=$( cd "$(dirname "$0")" ; pwd -P )

docker-compose --env-file "$FILE_PATH/.prod.env" -f "$FILE_PATH/docker-compose.prod.yml" up -d
