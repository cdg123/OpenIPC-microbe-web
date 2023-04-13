![OpenIPC Logo](https://cdn.themactep.com/images/logo_openipc.png)

My fork to experiment with getting pan and tilt functions working for XM530
===========================================================================

As I had a small number of XM530 IP Cameras the only issue I had to using 
them in our site cctv coverage was that the pan and tilt functionilty had not
yet been implemented.

Luckily the building blocks are all there and so it was challenge accepted for 
me to learn about the existing code, javascript, css and server side coding with Ash.

This is very much focussed on my need to get Pan and Tilt working with the XM530 cameras
I have and so I hope by sharing it then it will be of some use to others who may find 
some elements of use.

I don't pretend to be an expert in CSS, Javascript etc. but have enough knowledge to have
bolted something together which works for me. There are my notes in the code which I hope
helps anyone trying to read it my approach and again I am sure there are better more
experienced people out there that can improve on my initial attempts. 


General Approach
================









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
