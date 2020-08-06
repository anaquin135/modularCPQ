# Kill any running containers
docker kill $(docker ps -q)

export mCPQ_DIR=$(pwd)

# Services
cd $mCPQ_DIR/services/authService
./startService.sh

cd $mCPQ_DIR/services/docService
./startService.sh

cd $mCPQ_DIR/services/oppService
./startService.sh

cd $mCPQ_DIR/services/prodService
./startService.sh

# Client
cd $mCPQ_DIR/client/flask
./startService.sh
