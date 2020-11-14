#!/usr/bin/env bash
[ -z "$HOSTNAME"        ] && { echo "Need to set HOSTNAME.";        }

shell=`basename $SHELL`
echo "Activating ROS..."
source /opt/ros/melodic/setup.$shell

echo "Setting up SDJL_ROOT..."
export SDJL_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Setting up PYTHONPATH..."
export PYTHONPATH=$SDJL_ROOT/catkin_ws/src:$PYTHONPATH

echo "Activating development environment..."
source $SDJL_ROOT/catkin_ws/devel/setup.$shell


echo "Setup ROS_HOSTNAME..."
export ROS_HOSTNAME=$HOSTNAME.local

echo "Setting ROS_MASTER_URI..."
if [ $# -gt 0 ]; then
    # provided a hostname, use it as ROS_MASTER_URI
    export ROS_MASTER_URI=http://$1.local:11311/
else
    echo "No hostname provided. Using $HOSTNAME."
    export ROS_MASTER_URI=http://$HOSTNAME.local:11311/
fi
echo "ROS_MASTER_URI set to $ROS_MASTER_URI"