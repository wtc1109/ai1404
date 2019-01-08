python -m py_compile *.py
python default_adv.py
rm bin/*
rm cgi-bin/*

rm -r ../data/
rm -r ../log/*

gcc -o ftok ftok.c
chmod 777 ftok
./ftok

mv ai2filter*.pyc bin/ai2filter.pyc
mv ai2getyuv*.pyc bin/ai2getyuv.pyc
mv Ai2Lamp*.pyc bin/Ai2Lamp.pyc
#mv aifilter*.pyc bin/aifilter.pyc
mv configfiles*.pyc bin/configfiles.pyc
mv createmdb*.pyc bin/createdb.pyc
mv led_displayer*.pyc bin/led_displayer.pyc
mv multi_ucmq*.pyc bin/multi_ucmq.pyc
#mv mono_ucmq*.pyc bin/mono_ucmq.pyc
mv rmfiles*.pyc bin/rmfiles.pyc
mv udpbroad0.pyc bin/udpbroad0.pyc
mv udpbroad1.pyc bin/udpbroad1.pyc
#mv userjpg*.pyc bin/userjpg.pyc
#mv origjpg*.pyc bin/origjpg.pyc
mv yuvfilter*.pyc bin/yuvfilter.pyc
mv wdt.pyc bin/wdt.pyc
mv wdt2.pyc bin/wdt2.pyc
mv ai_init*.pyc bin/ai_init.pyc
mv auto_reboot.pyc bin/auto_reboot.pyc
mv mrtsp3.pyc bin/mrtsp.pyc
#mv amqp_consumer.pyc bin/amqp_consumer.pyc
mv amqp_consumer*.pyc bin/amqp_consumer.pyc
mv amqp_bind2.pyc bin/amqp_bind.pyc
#mv jpgcomment.pyc bin/jpgcomment.pyc
mv reboot_offline.pyc bin/reboot_offline.pyc
mv set_lamp.pyc bin/set_lamp.pyc



#mv h264*.pyc bin/h264.pyc

mv aiversion*.pyc cgi-bin/aiversion.pyc
mv allonlinehvpd*.pyc cgi-bin/allonlinehvpd.pyc
mv allonlineled*.pyc cgi-bin/allonlineled.pyc
mv downloadai*.pyc cgi-bin/downloadai.pyc
mv downloadled*.pyc cgi-bin/downloadled.pyc
mv downloadhvpd*.pyc cgi-bin/downloadhvpd.pyc
mv cgi_hvpd1.pyc cgi-bin/hvpd1list.pyc
mv cgi_hvpd2.pyc cgi-bin/hvpd2list.pyc
mv cgi_hvpd3.pyc cgi-bin/hvpd3list.pyc
mv cgi_hvpd4.pyc cgi-bin/hvpd4list.pyc
mv cgi_hvpd5.pyc cgi-bin/hvpd5list.pyc
mv cgi_hvpd6.pyc cgi-bin/hvpd6list.pyc
mv cgi_playmp4.pyc cgi-bin/playmp4.pyc
mv cgi_backDB.pyc cgi-bin/backupsql.pyc
mv cgi_recoveryFDB.pyc cgi-bin/recoveryfile.pyc
mv cgi_recoveryLDB.pyc cgi-bin/recoverylocal.pyc
mv cgi_bayusing.pyc cgi-bin/bay_using.pyc
mv cgi_vlpr_cur.pyc cgi-bin/vlpr_cur.pyc
mv cgi_vlpr_cur2.pyc cgi-bin/vlpr_cur2.pyc
mv cgi_adv.pyc cgi-bin/adv.pyc
#mv cgi_device_service.pyc cgi-bin/device_service.pyc
#mv cgi_vcap.pyc onvif/device_service.pyc


python softversion.py
rm softversion.pyc

cp wtclib.pyc bin/wtclib.pyc
cp openRTSP bin/rtsp_client
cp reboot_upgrade.zip bin/
cp hvpd_status.pyc bin/hvpd_status.pyc
cp ftok bin/
cp adv_set.db bin/


cp bin/* /home/bluecard/mhvpd/prog/bin/
cp cgi-bin/* /home/bluecard/mboa/www/cgi-bin/
#cp onvif/* /home/bluecard/boa/www/onvif/

cp index.html /home/bluecard/boa/www/
cp recoveryDB.html /home/bluecard/boa/www/


