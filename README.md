![OpenIPC Logo](https://cdn.themactep.com/images/logo_openipc.png)

Very much work in progress as tidying up files and remaking from sandpit code currently


My fork to get pan and tilt functions working for XM530
===========================================================================

As I had a small number of XM530 IP Cameras which I wanted to remove the 
original firmware from the only issue I had in using them in our site cctv 
coverage was that the pan and tilt functionilty had not yet been implemented 
within this OpenIPC software

Luckily I found the building blocks are all there and so it was challenge accepted for 
me to learn about the existing code, javascript, css and server side coding with 
a minimlist version of Bash. (Ash I believe).

This project is very much focussed on my need to get Pan and Tilt working with
the XM530 cameras I have and so I hope by sharing it then it will be of some use 
to others who may find some elements of use.

I don't pretend to be an expert in CSS, Javascript etc. but have enough knowledge to have
bolted something together which works for me. There are my notes in the code which I hope
helps anyone trying to read it my approach and again I am sure there are better more
experienced people out there that can improve on my initial attempts. 

Initial Objective
=================
- Create a Pan and Tilt GUI interface to be able to position the cameras on initial installation
- Be able to get the camera status and its current location
- Try to re-use existing CSS, JS functions where possible
- See if there is an option to set a small number of presets (original firmware allows this through VLC and OnVif)

General Approach
================
The concept of my thinking is quite simple; draw a number of arrows which each use an event listener to send a command
to a server side cgi module that in turn passes the required command string to the XM-Kmotor module.

Enchance the XM-Kmotor module with two new options (-j -i) to send back a JSON formatted string to be able to get camera
status, current location and the max X and Y parameters.

See the motors repository readme on how to ensure the kmotor module is added to the existing setup.

I found that on my camera the R80X20-PQ, which has a SC2315e (sc307e) sensor, that the X and Y degrees needed to be changed
to 280 and 127 which gave a maximum steps Y of 1444 and X of 3185 
(original is insmod /lib/modules/3.10.103\+/xiongmai/kmotor.ko gpio_pin=3,70,75,77,74,76,69,71,-1,-1,-1,-1 auto_test=1 MAX_DEGREE_X=350 MAX_DEGREE_Y=125)

PTZ Gui
=======
To try and decouple the ptz functionality initially from the preview.cgi page I decided to create this standalone and then include it into the preview.cgi as I thought this would allow easier debugging and more flexible if the preview page went therough any major updates or changes.

As the XM530 camera I have does not have zoom functionality then it is simply pan and tilt that I have completed.

I also wanted a speed option and so used a vertical slider control to adjust the number of steps per direction click event and the camera speed setting for pan/tilt.   

These are all scripted within the file xm530ptzclient.cgi




From original:
microbe-web
===========

Microbe is a web interface for [OpenIPC Firmware][openipcfw],
and is available on port 85 of your camera.

Default credentials to access the web interface are: username _admin_, and
password _12345_. You will be asked to change the password at the first login.
Please note that this will also assign the same password to user _root_!

### Support

OpenIPC offers two levels of support.

- Free support through the community via [chat][telegram].
- Paid commercial support directly from the team of developers.

Please consider subscribing for paid commercial support if you intend to use our
product for business. As a paid customer, you will get technical support and
maintenance services directly from our skilled team. Your bug reports and
feature requests will get prioritized attention and expedited solutions. It's a
win-win strategy for both parties, that would contribute to the stability your
business, and help core developers to work on the project full-time.

If you have any specific questions concerning our project, feel free to
[contact us](mailto:dev@openipc.org).

### Participating and Contribution

If you like what we do, and willing to intensify the development, please
consider participating.

You can improve existing code and send us patches. You can add new features
missing from our code.

Please make changes against the `dev` branch of the project, that's where the
most recent code resides. Keep your codebase fresh pulling changes from the
repo frequently, merging them into your local repo, and rebasing your code to
eliminate conflicts. Remember that you write for embedded linux thus please keep
your code as small and opimized as possible. Avoid using extra libraries like
jQuery, pure JavaScript is quite enough. Use valid HTML5 code. Avoid using
deprecated tags and attributes.

You can help us to write a better documentation, proofread and correct our
websites.

You can just donate some money to cover the cost of development and long-term
maintaining of what we believe is going to be the most stable, flexible, and
open IP Network Camera Framework for users like yourself.

You can make a financial contribution to the project at [Open Collective][oc].

Thank you.

<p style="text-align:center"><a href="https://opencollective.com/openipc/contribute/backer-14335/checkout" target="_blank"><img src="https://opencollective.com/webpack/donate/button@2x.png?color=blue" width="375" alt="Open Collective donate button"></a></p>

[openipcfw]: https://github.com/OpenIPC/firmware
[haserl]: http://haserl.sourceforge.net/
[iso639]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[wiki]: https://github.com/OpenIPC/firmware/wiki/microbe-web
[telegram]: https://openipc.org/#telegram-chat-groups
[oc]: https://opencollective.com/openipc/contribute/backer-14335/checkout
[pp]: https://www.paypal.com/donate/?hosted_button_id=C6F7UJLA58MBS
