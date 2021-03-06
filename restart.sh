GATEWAY=`ps -ef|grep gateway.py|grep -v grep|awk '{print $2}'`
for pid in $GATEWAY
do
  kill -9 $pid
done

WEBSOCK=`ps -ef|grep websock.py|grep -v grep|awk '{print $2}'`
for pid in $WEBSOCK
do
  kill -9 $pid
done

(python3 websock.py)&
python3 gateway.py