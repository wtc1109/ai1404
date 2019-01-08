python -m py_compile *.py

rm cgi-bin/*

cp adv.sh get.sh
cp adv.sh get2.sh
cp adv.sh show.sh
cp adv.sh upgrade.sh

echo "python get.pyc">>get.sh
echo "python get2.pyc">>get2.sh
echo "python show.pyc">>show.sh
echo "python upgrade.pyc">>upgrade.sh

mv cgi_get.pyc cgi-bin/get.pyc
mv cgi_get2.pyc cgi-bin/get2.pyc
mv cgi_show.pyc cgi-bin/show.pyc
mv cgi_upgrade.pyc cgi-bin/upgrade.pyc
#mv cgi_hvpd5.pyc cgi-bin/hvpd5list.pyc
#mv cgi_hvpd6.pyc cgi-bin/hvpd6list.pyc
#mv cgi_hvpd7.pyc cgi-bin/hvpd7list.pyc


mv get.sh cgi-bin/
mv get2.sh cgi-bin/
mv show.sh cgi-bin/
mv upgrade.sh cgi-bin/
