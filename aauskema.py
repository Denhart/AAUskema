#!/usr/bin/python
#Parser for calmoodle, Python3
#Written by Denhart @ http://denhart.dk
#This code is public domain. 
import argparse
import shutil
import datetime 
from urllib.request import urlopen
from urllib.error import URLError
from xml.dom import minidom 
from prettytable import *
 
parser = argparse.ArgumentParser(description='Calmoodle Parser.',epilog="Written by Denhart @ http://denhart.dk")
parser.add_argument('-o','--offset', metavar='int', type=int,default=0, help='offset current week (default = 0)')
parser.add_argument('url',default=0, help='url to moodle XML file')
parser.add_argument('--cache','-c' ,default='skema.xml', help='cache save (default = skema.xml)')
args = parser.parse_args()
try:
  skemaxml = urlopen(args.url, timeout = 5)
  #Save cachefile
  with open(args.cache, 'wb') as fp:
    shutil.copyfileobj(skemaxml, fp)
except URLError:
  pass
  
#Get week number
currentweek = int(datetime.date.today().isocalendar()[1])+args.offset
#Read raw xml data to parse. 
xmldoc = minidom.parse(args.cache)
kursusgang = xmldoc.getElementsByTagName("kursusgang") 
prettyTable = PrettyTable(["Day", "Course", "Location", "Time"])
prettyTable.align["Day"] = "l"
prettyTable.align["Course"] = "l"
prettyTable.align["Location"] = "l"
for element in kursusgang:
  weeknumber = int(element.getElementsByTagName("uge")[0].firstChild.data)
  if weeknumber == currentweek:
    try:
      lokale = element.getElementsByTagName("lokale-navn")[0].firstChild.nodeValue
    except:
      lokale = "N/A"
      pass
    kursusnavn = element.getElementsByTagName("kursus-navn")[0].firstChild.nodeValue
    #if ("Control Engineering" and "Informatics") not in str(kursusnavn):
    if ("Control Engineering" not in str(kursusnavn)) and ("Informatics" not in str(kursusnavn)) :
      kursusnavn = str(kursusnavn.split("(")[0])
      if "Introduction to Probability Theory and Statistics" in kursusnavn:
        kursusnavn = str("Probability Theory")
      if "Matrix Computations and Convex Optimization" in kursusnavn:
        kursusnavn = str("Matrix Computations")
      if "Electronic Engineering and IT 6" in kursusnavn:
        kursusnavn = str("EIT 6")
    
      if "ESB" in str(lokale):
        regex = re.compile("""AAU: (.*) / ESB""")
        temp = regex.findall(lokale)
        lokale = temp[0]
      kursusdag = str(element.getElementsByTagName("dag")[0].firstChild.data)
      kursusdag+=str(":")
      kursusstart = element.getElementsByTagName("time-start")[0].firstChild.data
      kursusslut = element.getElementsByTagName("time-slut")[0].firstChild.data
      #print("{:10} {:33} {}".format(kursusdag,kursusnavn, kursusstart))
      prettyTable.add_row([kursusdag,kursusnavn,lokale,kursusstart])
print(prettyTable)