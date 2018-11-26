============
CSS and Less
============

Oscar uses Less to build its CSS files.  Each of the 3 main CSS files has a
corresponding less file::

    styles.less -> styles.css
    dashboard.less -> dashboard.css

Oscar's CSS uses Less files from the `Bootstrap project`_ - these are housed
in the bootstrap folder.

.. _`Bootstrap project`: http://getbootstrap.com/

Compiling less
--------------

You can compile the CSS from the root of the project using a make target::
    
    make css
