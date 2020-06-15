# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana 

NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.

2. Move Implementation.

  The first method is:
 define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function.
  
  The second method is:
 mv function can be also got by motor.move(val=int(position)).



3. Version update(debian9 to debian 10)
https://www.cyberciti.biz/faq/update-upgrade-debian-9-to-debian-10-buster/


java 11 to java 8
https://linuxize.com/post/install-java-on-debian-10/
