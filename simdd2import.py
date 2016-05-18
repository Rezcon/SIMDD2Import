#!/usr/bin/python

import urllib2, base64, urllib, csv
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

pathToSimFile = "/Users/bpopejoy/Documents/SIMDD2.txt"
username = ""
passowrd = ""

def updateStudentInfo(redID, enrollmentStatus):
	request = urllib2.Request("https://oncampuslivingtest.sdsu.edu/StarRezRESTtest/services/select/entry.xml?id1=" + redID)
	base64string = base64.encodestring('%s:%s' % (username, passowrd)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	try:
		handler = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		print "HTTPError = " + str(e.code)
	except urllib2.URLError, e:
		print "URLError = " + str(e.reason)
	except httplib.HTTPException, e:
		print 'HTTPException'
	except Exception:
		import traceback
		print 'generic exception: ' + traceback.format_exc()
	else:
		response = handler.read()
		root = ET.fromstring(response)
		entryID = root[0][0].text
		request = urllib2.Request("https://oncampuslivingtest.sdsu.edu/StarRezRESTtest/services/select/entrycustomfield.xml?entryid=" + entryID + "&customfielddefinitionid=1096")
		base64string = base64.encodestring('%s:%s' % (username, passowrd)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)
		try:
			handler = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
			print "URLError = " + str(e.reason)
		except httplib.HTTPException, e:
			print 'HTTPException'
		except Exception:
			import traceback
			print 'generic exception: ' + traceback.format_exc()
		else:
			response = handler.read()
			root = ET.fromstring(response)
			fieldID = root[0][0].text
			request = urllib2.Request("https://oncampuslivingtest.sdsu.edu/StarRezRESTtest/services/update/entrycustomfield/" + fieldID)
			data = urllib.urlencode({'valuestring' : enrollmentStatus})
			base64string = base64.encodestring('%s:%s' % (username, passowrd)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string)
			try:
				handler = urllib2.urlopen(request, data)
			except urllib2.HTTPError, e:
				print "HTTPError = " + str(e.code)
				print e.read()
			except urllib2.URLError, e:
				print "URLError = " + str(e.reason)
			except httplib.HTTPException, e:
				print 'HTTPException'
			except Exception:
				import traceback
				print 'generic exception: ' + traceback.format_exc()
			else:
				print redID + ' - Success'

def main():
	with open(pathToSimFile, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			redID = row[0]
			enrollmentStatus = row[7]
			updateStudentInfo(redID, enrollmentStatus)

main()