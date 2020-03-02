Personal Mac Fan Controller
======
This is a package that I am putting together to help control my Mac's fans on Ubuntu. There's still a ton to get done with this, but it's coming along nicely.

#### Todo List

* Command line options
  * Command line options are in preparation for the GUI. 
    * GUI would have the different windows for creating configs, and selecting configs. 
    * I want to be able to streamline the process of creating multiple configs for (percentages, charging, discharging)
  * Config file.
    * Find a way to write config files.
    * **Different temperature ranges based on battery status (percentages, charging, discharging)**
    * ~The config file would allow for different temperature ranges.~
    * ~The config file would allow for different fan speeds for these different temperature ranges.~
    * ~**(This shit is going to take so long) (I lied! Didn't look at it right.)**~
  * ~`Debug` option.~
* ~Separating the script into root and normal user sections~
  * ~The user script will have sensor readings and fan speed.~
  * ~The root script would add control to the fan.~
