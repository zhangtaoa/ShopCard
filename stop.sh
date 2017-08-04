procnum=`ps -ef|grep python|grep shopCard|grep -v grep|wc -l`

if [ $procnum -gt 0 ]
then
   procnum=`ps -ef|grep python|grep shopCard|grep -v grep|awk '{print $2}'` 
   echo "Stop Process Pid:" $procnum
   kill -9 $procnum
else
   echo "No Process Run"
fi
