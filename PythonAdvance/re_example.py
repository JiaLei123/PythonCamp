import re

pattern = re.compile(r'[0-9]+')
match = pattern.findall('hello world! hello')
print pattern.findall('station 1000 100 and 7')



