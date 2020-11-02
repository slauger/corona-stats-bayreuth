#!/usr/bin/env python3
#
# Corona Data Extrator for landkreis-bayreuth.de

import re
import json
import requests
import dateutil.parser
import sys

baseurl = 'https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/'

def translate_month(string):
  dictionary = {
    'Januar': 'January',
    'Februar': 'February',
    'März': 'March',
    'Mai': 'May',
    'Juni': 'June',
    'Juli': 'July',
    'Oktober': 'October',
    'Dezember': 'December',
  }
  for key in dictionary.keys():
    string = string.replace(key, dictionary[key])
  return string

response = requests.get(baseurl)
result   = re.findall('<a href="/der-landkreis/pressemitteilungen/corona-fallzahlen-([0-9]+)/">', response.text)
result   = sorted(result, reverse=True)

all_data = []

for page in result:
  url = baseurl + '/corona-fallzahlen-{}'.format(page)
  response = requests.get(url)

  # parse
  parsed_date = dateutil.parser.parse(translate_month(re.findall('(Corona-F\&\#228;lle in Stadt und Landkreis Bayreuth am|am) ([0-9]+\. [A-Za-z]+ [0-9]+)', response.text)[0][1]))

  incidence_rate = re.findall('Die 7-Tage-Inzidenz betr\&\#228;gt im Landkreis ([0-9]+,[0-9]+) und in der Stadt Bayreuth ([0-9]+,[0-9]+)', response.text)
  if incidence_rate:
    incidence_rate = incidence_rate[0]
  else:
    incidence_rate = ["0", "0"]

  infected_current = re.findall('(Im Landkreis sind heute|Aktuell sind im Landkreis) ([0-9]+) und in der Stadt Bayreuth ([0-9]+) Personen nachweislich mit dem Corona-Virus CoV-2 infiziert.', response.text)
  if infected_current:
    infected_current = infected_current[0]
  else:
    infected_current = re.findall('Aktuell sind in Stadt und Landkreis Bayreuth jeweils ([0-9]+) Personen nachweislich mit dem Corona-Virus CoV-2 infiziert.', response.text)
    infected_current = [None, "0", "0"]

  patients = re.findall('Insgesamt ([0-9]+) Patienten, davon ([0-9]+) aus Stadt und Landkreis Bayreuth, werden derzeit stationär in einer Klinik wegen COVID_19 behandelt.', response.text)
  if patients:
    patients = patients[0]
  else:
    patients = ["0", "0"]

  infected_total = re.findall('Seit Ausbruch der Pandemie wurden insgesamt im Landkreis ([0-9]+) und in der Stadt Bayreuth ([0-9]+) Personen positiv auf dieses Corona-Virus getestet.', response.text)[0]
  deaths = re.findall('([0-9]+) Patienten aus dem Landkreis sowie ([0-9]|zehn) aus der Stadt Bayreuth sind bisher an den Folgen der Infektionskrankheit COVID-19 verstorben.', response.text)[0]
  recovered = re.findall('Als genesen gelten ([0-9]+) Personen aus dem Landkreis und ([0-9]+) aus der Stadt, darunter sowohl Personen, die mit typischer Symptomatik erkrankt gewesen waren, aber auch solche, bei denen trotz fehlender Krankheitszeichen ein positiver Test auf CoV-2 vorgelegen hatte.', response.text)[0]

  data = {
    'date': str(parsed_date),
    'inzidenz': {
      'land': float(incidence_rate[0].replace(",", ".")),
      'stadt': float(incidence_rate[1].replace(",", "."))
    },
    'infected': {
      'current': {
        'land': int(infected_current[1]),
        'stadt': int(infected_current[2])
      },
      'total': {
        'land': int(infected_total[0]),
        'stadt': int(infected_total[1]),
      }
    },
    'patients': {
      'total': int(patients[0]),
      'local': int(patients[1]),
    },
    'deaths': {
      'land': int(deaths[0]),
      'stadt': int(deaths[1].replace("zehn", "10")),
    },
    'recovered': {
      'land': int(recovered[0]),
      'stadt': int(recovered[1]),
    }
  }

  all_data.append(data)

  if len(sys.argv) > 2:
    if sys.argv[1] == '-a':
      continue
    else:
      break
  else:
    break

print(json.dumps(all_data))
