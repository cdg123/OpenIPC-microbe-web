#!/usr/bin/haserl
<%in p/common.cgi %>

<% page_title="PTZ Handler" %>
<%
#This is designed as an async call from within preview.cgi i.e. not directly
#So first check we have parameters passed in and if not simply call the xm-kmotor module
#which will return the current settings 

*** ToDo add logic to handle direct call from command line etc. ****

#we should have an event posted at this point from the client browser ptz control
#if not then set the action to empty string and return 

#need to set speed setting as set with slider control
#need to be careful not to drive motor beyond max as this messes up the real vs counted in here x,y pos

#Usage : xm-kmotor -d + i j for json response
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

ptz_action="xm-kmotor" #default if not posted data from a form so probably not an ajax request or from cmd line


case "$FORM_ptzcmd" in
   ptzinit)
   ptz_action="xm-kmotor -i"  
   ;;

   ptzstatus)
   ptz_action="xm-kmotor -j"  
   ;;

   
   ptzgoto)
   ptz_action="xm-kmotor -d t -s $FORM_speed -x $FORM_xpos -y $FORM_ypos"
   ;;
 
    ptzst) #stop
    ptz_action="xm-kmotor -d s"
    ;;

   ptzsu) #step up -d g -x0 -y10
    ptz_action=""
    ;;
  
  ptzsul) #step up left **** how can we step in a negative way ?? Can workaround using goto x,y
    ptz_action="xm-kmotor -d s" #stop for now
    ;;

  ptzsur) #step up right -d g -x10 -y10
    ptz_action=""
    ;;

  ptzsl) #step left **** how can we step in a negative way ?? Can workaround using goto x,y
    ptz_action="xm-kmotor -d ss" #stop for now
    ;;

  ptzsr) #step right
    ptz_action="xm-kmotor -d s"
    ;;


  ptzsd) #step down **** how can we step in a negative way ?? Can workaround using goto x,y
    ptz_action="xm-kmotor -d s"
    ;;
  *)
    ptz_action = "xm-kmotor"
    ;;
esac


# ****** send to camera *****
result=$(eval $ptz_action)

if [ "ptzinit" != "$FORM_ptzcmd" ]; then
  # if the action is not ptzinit then we need to get status
  # as camera could still be moving
  ptz_action="xm-kmotor -j"
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