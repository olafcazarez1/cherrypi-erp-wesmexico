SERVICE='cherrypi-cafe88.py\s --config-file'
SCRIPT_PATH=$(dirname `which $0`)

while true
	do

		if ps -AF | grep -v grep | grep -e 'cherrypi-cafe88.py --config-file' > /dev/null
		then
			sleep 2
			continue
		else
			python3.12 $SCRIPT_PATH/cherrypi-cafe88.py --config-file $SCRIPT_PATH/conf/default.conf&
			sleep 5
		fi
done
