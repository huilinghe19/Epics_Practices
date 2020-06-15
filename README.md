# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana 

NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.

2. Move Implementation.

  The first method is:
 define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function.
  
  The second method is:
 mv function can be also got by motor.move(val=int(position)).



3. Version update

debian9 to debian 10:
https://www.cyberciti.biz/faq/update-upgrade-debian-9-to-debian-10-buster/


java 11 to java 8:
https://linuxize.com/post/install-java-on-debian-10/

4. 
# remove all taurus version at first. install taurus on debian 10 as follows:

https://taurus-scada.org/users/getting_started.html

# install taurus in develop mode
git clone https://github.com/taurus-org/taurus.git

sudo pip3 install -e ./taurus  

# install taurus_pyqtgraph in develop mode
git clone https://github.com/taurus-org/taurus_pyqtgraph.git

sudo pip3 install -e ./taurus_pyqtgraph  

5. 
# install itango3 with python3 :

uninstall all version. install from this way: sudo apt install python3-itango

# install sardana unter python3
Working directly from Git

If you intend to do changes to Sardana itself, or want to try the latest developments, it is convenient to work directly from the git source in “develop” (aka “editable”) mode, so that you do not need to re-install on each change.

You can clone sardana from the main git repository:

git clone https://github.com/sardana-org/sardana.git sardana

Then, to work in editable mode, just do:

sudo pip3 install -e ./sardana



