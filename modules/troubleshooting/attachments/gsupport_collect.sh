#!/bin/bash

# TigerGraph Support Collector v1.2
# Revised 6/1/2022
TIME_IN_PAST=86400 # 60 * 60 * 24 hours
INSTALL_DIR="/home/tigergraph/tigergraph/app/cmd"
supportdir="support_collection_$(date +%F_%H%M%S)"

Usage(){
  echo ""
  echo "TigerGraph Support Collection Tool"
  echo ""
  echo "Usage: $(basename "$0") [-t <seconds]"
  echo "  -t : time, in seconds, for historical log duration"
  echo "       default is 86400 seconds (or 24 hours)"
  echo " "
  echo "Example:"
  echo "  '$(basename "$0") -t 3600'  : Run this command for logs for last 3600 seconds (60 mins or 1 hour)"
  exit 1
}

while [ -n "$1" ];
do
  case "$1" in
    -t)
      shift
      TIME_IN_PAST=$1
      ;;
    *)
      Usage
      exit 0
      ;;
  esac
  shift
done

if [ ! -e "${INSTALL_DIR}"/gcollect ]; then
  echo "Can't access ${INSTALL_DIR}/gcollect. Check TigerGraph software installation"
  exit 1
fi
echo "Collecting logs/config for last ${TIME_IN_PAST} seconds"
gcollect -o ./"$supportdir" -t "${TIME_IN_PAST}" collect
STATUS=$?

if [ ${STATUS} -ne 0 ]; then
  echo "Error: gcollect command failed to execute"
  exit 1
fi


echo; echo "Collecting current state..."
{
  printf "\n===gssh===\n"
  gssh
  printf "\n===gstatusgraph==="
  gstatusgraph
  printf "===GPE binary checksum==="
  grun_p all "md5sum $(gadmin config get System.AppRoot)/bin/tg_dbs_gped"
  printf "\n===System Date==="
  grun_p all "date"
  printf "\n===TG Process State==="
  grun all "ps aux | grep $(gadmin config get System.AppRoot)/bin/"
  printf "\n===Top Processes==="
  grun all "top -b -n 1 | head -n 25"
  printf "\n===CPU Architecture Information==="
  grun all "lscpu"
  printf "\n===disks==="
  grun all "lsblk -d -e 7 -o name,rota"
} > "${supportdir}"/support.log 2>&1

echo; echo "Compressing support bundle collection (this may take some time)..."
tar -Jcf "$supportdir".tar.xz "$supportdir"; rm -rf "$supportdir"

#ZenDesk has file upload limit of 50MB.
#check the size of the bundle, if it is more than 50MB, then split file into multiple chunks

collectionsize=$(du -s "$supportdir".tar.xz | cut -f1); uploads=$(((collectionsize/500000)+1))
if [ $uploads -ne 1 ]; then
  echo; echo "Due to upload size limits, the support bundle will be split into $(((collectionsize/500000)+1)) peices."
  mkdir "$supportdir";
  split --verbose -d -b 50M "$supportdir".tar.xz "$supportdir"/"$supportdir".tar.xz.part;
  rm "$supportdir".tar.xz;
  echo; echo "Support Collection has been saved under $supportdir directory."
else
  echo; echo "Support Collection has been saved as $supportdir.tar.xz"
fi