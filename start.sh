. $HOME/.bash_profile

if [ $# -lt 1 ]
then
   #echo "Usage:start.sh port"
   #exit 1
   echo "Use default port [51800]"
   port=51800
else
   port=$1
fi

workdir=`pwd`

procnum=`ps -ef|grep python|grep shopCard|grep -v grep|wc -l`

if [ $procnum -lt 1 ]
then
nohup python $workdir/shopCard.py --port=$port --rundir=$workdir >/dev/null 2>&1 &
fi
