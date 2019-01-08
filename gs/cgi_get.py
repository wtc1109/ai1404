import cgi, json

form = cgi.FieldStorage()
_dict1 = {"ret":"ok"}
for key in form.keys():
    _dict1.update({key:form[key].value})

print "Content-type:text/html\n\n"
print json.dumps(_dict1)