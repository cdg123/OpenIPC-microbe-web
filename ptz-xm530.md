Very much work in progress as tidying up files and remaking from sandpit code currently

My fork to get pan and tilt functions working for XM530
As I had a small number of XM530 IP Cameras which I wanted to remove the original firmware from the only issue I had in using them in our site cctv coverage was that the pan and tilt functionilty had not yet been implemented within this OpenIPC software

Luckily I found the building blocks are all there and so it was challenge accepted for me to learn about the existing code, javascript, css and server side coding with a minimlist version of Bash. (Ash I believe).

This project is very much focussed on my need to get Pan and Tilt working with the XM530 cameras I have and so I hope by sharing it then it will be of some use to others who may find some elements of use.

I don't pretend to be an expert in CSS, Javascript etc. but have enough knowledge to have bolted something together which works for me. There are my notes in the code which I hope helps anyone trying to read it my approach and again I am sure there are better more experienced people out there that can improve on my initial attempts.

Initial Objective
Create a Pan and Tilt GUI interface to be able to position the cameras on initial installation
Be able to get the camera status and its current location
Try to re-use existing CSS, JS functions where possible
See if there is an option to set a small number of presets (original firmware allows this through VLC and OnVif)
General Approach
The concept of my thinking is quite simple; draw a number of arrows which each use an event listener to send a command to a server side cgi module that in turn passes the required command string to the XM-Kmotor module.

Enchance the XM-Kmotor module with two new options (-j -i) to send back a JSON formatted string to be able to get camera status, current location and the max X and Y parameters.

See the motors repository readme on how to ensure the kmotor module is added to the existing setup.

I found that on my camera the R80X20-PQ, which has a SC2315e (sc307e) sensor, that the X and Y degrees needed to be changed to 280 and 127 which gave a maximum steps Y of 1444 and X of 3185 (original is insmod /lib/modules/3.10.103+/xiongmai/kmotor.ko gpio_pin=3,70,75,77,74,76,69,71,-1,-1,-1,-1 auto_test=1 MAX_DEGREE_X=350 MAX_DEGREE_Y=125)

PTZ Gui
To try and decouple the ptz functionality initially from the preview.cgi page I decided to create this standalone and then include it into the preview.cgi as I thought this would allow easier debugging and more flexible if the preview page went therough any major updates or changes.

As the XM530 camera I have does not have zoom functionality then it is simply pan and tilt that I have completed.

I also wanted a speed option and so used a vertical slider control to adjust the number of steps per direction click event and the camera speed setting for pan/tilt.

These are all scripted within the file xm530ptzclient.cgi

From original: microbe-web
