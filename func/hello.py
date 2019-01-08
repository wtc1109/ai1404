#!/usr/bin/python
import cgi, cgitb

form = cgi.FieldStorage()
first_name = form.getvalue("first_name5")
last_name = form.getvalue("last_name5")
print "Content-type:text/html\n\n"
print "<html>"
print "<head>"
print "<title>12345678</title>"
print "<body>"
print "asfdhu"
print "fisrt5 = ",first_name
print "last5 = ", last_name
print "</body>"
print "</html>"