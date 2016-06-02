plonecontent
============

XBLOCK to show Content from a Plone-Site in MOOCs based on OPENedX
------------------------------------------------------------------

Plone is a free Web Content-Management-System. For more information see Plone-Homepage.

With this XBlock you can show content-objects hosted on a Plone-Site within an Online-Course. For example if you have some documents from a knowledge database and you are interested in to integrate these documents in your course-flow without any external styles, logos, colors, etc. you can use "plonecontent". plonecontent is the alternative way to use the iFrame XBlock for such usecases. The XBlock plonecontent connects to the foreign server via a http connection and needs as special softwarepacke plone.restapi which provides a RESTful Webservice on the other side to read the content data from Plone.


Requirements on Plone-Side
--------------------------

CMF Plone >= 4.3
plone.restapi (https://github.com/plone/plone.restapi)


Installation
------------

**Move to the folder where you want to download the plonecontent XBlock**

cd /edx/app/edxapp

**Download the XBlock**

sudo -u edxapp git clone https://github.com/educorvi/plonecontent.git

**If not installed: Install the XBlock**

sudo -u edxapp /edx/bin/pip.edxapp install plonecontent/

**Remove the installation files**
sudo rm -r plonecontent

Hinweis:
Maybe the edxapp User has not enough rights to install the XBlock Requirement "restclient" and your got a error during the installation process. I recommend to install the restclient package with your Installation-User (maybe vagrant) or with superuser privileges:
sudo /edx/bin/pip.edxapp restclient

Within your course:

Goto Settings --> Advanded Settings and modify the "Advanced Module List": ["plonecontent",]

