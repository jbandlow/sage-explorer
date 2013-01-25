Sage Explorer: a tool for exploring Sage objects and connections between them

It displays a Sage object, some relevant information about this
object, and links to related objects (those that can be obtained using
a method of the object).  One central feature of the tool is to make
it easy to configure which piece of information is relevant, typically
depending on the semantic of the object.

	  https://github.com/jbandlow/sage-explorer
	  https://explore.sagemath.org (some day)

How to run it
-------------

You need sage installed (http://sagemath.org). Then, from the
Sage Explorer directory, run:

    > sage -python sage_explorer

and connect to the URL that is mentioned (typically http://127.0.0.1:5000/)

WARNING: AT THIS POINT NO STEP HAS BEEN TAKEN TOWARD SECURITY

By choosing appropriate url's, the user can trivially run any sage
command -- and in particular any shell command -- on the server under
the web server's uid. Use locally or at your own risks.

Motivation for this prototype
-----------------------------

The current prototype was implemented by Jason Bandlow and Nicolas
M. Thiéry during the AIM/ICMS workshop:

    Online databases: from L-functions to combinatorics

The purpose was to evaluate whether such a tool could be written as a
thin view layer above Sage, and how much the semantic information
available in Sage was useful and sufficient for that purpose.

Implementation
--------------

Sage Explorer is currently implemented as a standalone web-site. Some
care was taken to separate the view (implemented using jinja
templates) from the model. It could therefore, in principle, work
generically as a web or heavy-weight GUI application (using QT or so).

Future
------

The two authors are unlikely to lead further development of this tool,
since they don't have a strong need for it themselves. If you think
this is useful, patches and take overs are very welcome.

For more, see the TODO list.
