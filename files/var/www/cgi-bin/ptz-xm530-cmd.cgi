#!/usr/bin/haserl

<% page_title="PTZ Handler" %>
<%
# This is designed as an async call from within preview.cgi i.e. not directly
# So first check we have parameters passed in and if not simply call the xm-kmotor module
# which will return the current settings 

*** ToDo add logic to handle direct call from command line etc. ****

# we should have an event posted at this point from the client browser ptz control
# we could check referer value is our client
# if not then set the action to empty string and return 

# need to set include speed setting as set with slider control
# we rely on max values for x and y being managed by the client

# We are just using the goto x, y for all moving around even thoguht eh xm-kmotor module will do all these..

# Usage : xm-kmotor -d + i j for json response
#         u (Up)
#         d (Down)
#         l (Left)
#         r (Right)
#         e (Right Up)
#         c (Right Down)
#         q (Left Up)
#         z (Left Down)
#         s (Stop)
#         h (Set position X and Y)
#         t (Go to X and Y)
#         f (Scan, Y to set)
#         g (Steps X and Y)

#logger "Post result for form is $POST_ptzcmd $POST_speed $POST_xpos $POST_ypos"

ptz_base="xm-kmotor" #base object to call


case "$POST_ptzcmd" in
   ptzinit)
   ptz_action="$ptz_base -i"
   ;;

   ptzstatus)
   ptz_action="$ptz_base -j"
   ;;

   ptzgoto)
   ptz_action="$ptz_base -d t -s $POST_speed -x $POST_xpos -y $POST_ypos"
   ;;

    ptzst) #stop
    ptz_action="$ptz_base -d s"
    ;;

  *)
    ptz_action = "$ptz_base"
    ;;
esac

# logger "ptz-command is $ptz_base"
# logger "ptz-command is now $ptz_action"

# ****** send to camera *****
result=$(eval $ptz_action)

if [ "ptzinit" != "$POST_ptzcmd" ]; then
  # if the action is not ptzinit then we need to get status
  # as camera could still be moving
  ptz_action="$ptz_base -j"
  result=$(eval $ptz_action)
#
fi

#send json string back to web page result in x and y positions
#Format to send json string back below once finished fixing and debugging

echo "HTTP/1.1 200 OK
#and set to json content type
Content-type: application/json; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(time_http)
Server: $SERVER_SOFTWARE
"
echo $result
%>