#!/usr/bin/haserl
<%in p/common.cgi %>

<%
if [ "/cgi-bin/xm530ptzclient.cgi" = "$REQUEST_URI" ]; then
  page_title="PTZ camera preview standalone"
  size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
  size_w=${size%x*}
  size_h=${size#*x}
%>
  <!DOCTYPE html>
  <html lang="<%= ${locale:=en} %>" data-bs-theme="<%= ${webui_theme:=light} %>">
  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title><% html_title %></title>
  <link rel="stylesheet" href="/a/bootstrap.css">
  <link rel="stylesheet" href="/a/bootstrap.override.css">
  <script src="/a/bootstrap.js"></script>
  <script src="/a/main.js"></script>
  </head>

  <body>
  <div class="row preview">
  <div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">
    <% preview 1 %>
    <p class="small text-body-secondary">The image above refreshes once per second and may appear choppy.
    To see a smooth video feed from the camera use one of the <a href="majestic-endpoints.cgi" target="_blank">video endpoints</a>.
  </div>
   <div class="col-md-4 col-xl-3 col-xxl-3">
    <div class="d-grid gap-2 mb-3">
<%
fi
%>

<link rel="stylesheet" href="/a/ptz.css">

<div class="ptzcontainer2" id="ptzform">
  <div class="box"><img src="/a/ptzFaster.svg" alt="Faster"></div>
  <div class="box-borderright"></div>
  <div class="box-ptzcolumn ptzimages">
  
  <a href="#" title="Step Up Left" id="ptzsul"><img src="/a/ptzUpLeft.svg" alt="Step Up Left"></a>
  <a href="#" title="Step Up" id="ptzsu"><img src="/a/ptzUp.svg" alt="Step Up"></a>
  <a href="#" title="Step Up Right" id="ptzsur"><img src="/a/ptzUpRight.svg" alt="Step Up Right"></a>
 <br>
 <a href="#" title="Step Left" id="ptzsl"><img src="/a/ptzLeft.svg" alt="Step Left"></a>
  <a href="#" title="Stop" id="ptzst"><img src="/a/ptzStop.svg" alt="Stop"></a>
  <a href="#" title="Step Right" id="ptzsr"><img src="/a/ptzRight.svg" alt="Step Right"></a>
<br>  
  <a href="#" title="Step Down Left" id="ptzsdl"><img src="/a/ptzDownLeft.svg" alt="Step Down Left"></a>
  <a href="#" title="Step Down" id="ptzsd"><img src="/a/ptzDown.svg" alt="Step Down"></a>
  <a href="#" title="Step Down Right" id="ptzsdr"><img src="/a/ptzDownRight.svg" alt="Step Down Right"></a>
   
   </div>

<!-- X here ***** -->
  <div class="box-borderleftrightbottom linesmall ptzXyText">X<br><input type="text" class="ptzTextbox" id="xpos" name="ptzxpos" tabindex="1">
  <!--need to trap going over max values <div class="ptzXyText">max:12</div> -->
  </div>
    <div class="input-group-text">
    <a href="#" title="PTZ settings"><img src="/a/gear.svg" alt="PTZ Settings"></a>
 </div>

  <div class="verticaltext x-small">speed</div>
  <div class="box-borderright">
   <div class="slider">
    <input type="range" min="1" max="10" value="5" step="1" id="speed" show="true">
    </div>
  </div>
  <!-- y here ***** -->
  <div class="box-borderleftrightbottom linesmall ptzXyText">Y<br><input type="text" class="ptzTextbox" id="ypos" name="ptzypos" tabindex="2"></div>
  <div class="input-group-text"></div>
  <div class="box-bottom"><img src="/a/ptzSlower.svg" alt="Slower"></div>
    <div class="box-borderright"></div>

  <div class="box-borderleftright"><input type="image" value="goto" id="ptzgoto" name="goto x,y" alt="go" src="/a/ptzGoto.svg" tabindex="3"></div>
  <div class="box"></div>
  <div class="box"></div>
  <div class="box-middle x-small" id="speed-show">5</div>
  <div class="box-bordertop x-small">x:<div class="status" id="camCurrentX" name="camCurrentX">123456</div>&nbsp;y:<div class="status" id="camCurrentY" name="camCurrentY">1234</div></div>
  <div class="box-bordertop x-small">status:<div class="status" id="ptzstatus" name="ptzstatus">moving</div></div>
  <div class="box-bordertop x-small"></div>
</div>

Click and hold buttons to pan<br />
ToDo: <ul>
<li>Better error checking for </li>
<li>How do we enable this? Need to check for this cam model and then display it ??</li>
<li>Need to update the script so action is configurable could then be used to point to different camera wrapper etc.</li>
<li>on page load event need to check kmotor module loaded else quit and alert user</li>
<li>Do we need any settings except enable/disable and where is this stored</li>
<li>Fix duplicate and unneaded css in my css and tune layout</li>
</ul>


<script>
//use on page load event to get the currrent x,y vals from the camera
//initially in case that fails, camera could be off etc then fill with 0,0
//could set these in the form but here ensures always reset to a value.
 
//get camera current values to set x,y vals to use in tracking
//The sendToXmotor function below returns a json string including status, xpos,ypos
//so we will use that to capture the current camera position on page load


//global vars 
//vars to track cam x,y
    let camX=0; //need these ?
    let camY=0; //need these ?
    let maxX=0;
    let maxY=0;
    let status=0;
    let steps=100; //seems a good value for each click of the direction buttons
    let speed=5; //options 1-10 
    let mymouseup=false;
    let xPos=0; //form values i.e. client side x and y 
    let yPos=0;

//runs on initial page load from eventlistener to ensure form elements exist
window.addEventListener('load', (event) => {

     
    //set the default x,y params on screen
    document.getElementById('xpos').value=camX;
    document.getElementById('ypos').value=camY;

    //contact the camera to pull off the max X and max Y params using -i option in updated xm-kmotor
    //console.log ("creating form ");
    const formData = new FormData();

    formData.append('ptzcmd', "ptzinit");

    //ensure gets sent as a URL encoded string as nothing sensitive like passwords
    const payload = new URLSearchParams(formData);

    //create async call   
    fetch("/cgi-bin/ptz-xm530-cmd.cgi", {
      method: "POST",
      body: payload,
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);

      //now keep the camera values to track for this session
      camX=data.xpos;
      camY=data.ypos;
      maxX=data.xmax;
      maxY=data.ymax;
      status=data.status; //65535 is when idle other values not known

      if (status==65535){
          statustxt="idle";
      }
      else{
        statustxt="moving";
      }

      document.getElementById('ptzstatus').innerHTML=statustxt;
      document.getElementById('camCurrentX').innerHTML=camX;
      document.getElementById('camCurrentY').innerHTML=camY;
    
    })

      .catch(err => console.log(err));
});


function waitms(ms){
  //function to use async await promise mechanism to use as a delay timer 
  //for checking camera status until current task completed
  return new Promise(resolve =>{
    setTimeout(()=>{ resolve('') }, ms);
  })
}

async function checkStatus(){
  //get camera status
  console.log("getting camera status");
  //console.log ("creating form ");
  const formData = new FormData();
  formData.append('ptzcmd', "ptzstatus");
  //ensure gets sent as a URL encoded string as nothing sensitive like passwords
  const payload = new URLSearchParams(formData);

  let loopcount=0;
  //start of loop to get camera status 
  do {
    //repeat check cam status every second 
    //wait 1 second and try again
    await waitms(500);
    
    console.log("getting status");

    fetch("/cgi-bin/xm530-ptz-wrap.cgi", {
      method: "POST",
      body: payload,
    })
    .then(res => res.json())
    .then(data => {
    
    console.log(data);
    camX=data.xpos;
    camY=data.ypos;
    status=data.status;
    console.log("status - %s", status);
    
    if (status==65535){ 
       statustxt="idle";
    }
    else{
      statustxt="moving";
    }
    console.log("statustxt - %s", statustxt);
     document.getElementById('ptzstatus').innerHTML=statustxt;
    document.getElementById('camCurrentX').innerHTML=camX;
    document.getElementById('camCurrentY').innerHTML=camY;

      })
      
        loopcount++;
        //do this for 5 seconds max i.e. 5 times TODO make it configurable
        //just needs to be slightly longer than time for camera to travel 0-max x ot y axis.
        //**** might need to include the speed setting for finer tuning / optimisation ******

        console.log("statustxt - %s", statustxt);

      } while (status<65535&&loopcount<20);
    }

function CalcXandY(x,y,xStep=0,yStep=0){ //pass in +x +y vals test against maxX, maxY and 0
  
  console.log ("calc x & y start");
  console.log ("x is ", x);
  console.log ("y is ", y);
  console.log ("xStep is ", xStep);
  console.log ("yStep is ", yStep);
  console.log ("xPos is ", xPos);
  console.log ("ypos is ", yPos);

  //if goto then xstep, ystep will be 0
  x=parseInt(x)+ parseInt(xStep); //x+=xStep
  y=parseInt(y)+ parseInt(yStep); //y+=yStep
  
  if (x>maxX){
     xPos=maxX;
  }
  else if (x<0) {
      xPos=0
  }
  else {
    xPos=x;
  };

   if (y>maxY){
     yPos=maxY;
  }
  else if (y<0) {
      yPos=0
  }
  else {
    yPos=y; 
  };

  console.log ("calc x & y end");
  console.log ("x is ", x);
  console.log ("y is ", y);
  console.log ("xPos is ", xPos);
  console.log ("ypos is ", yPos);

}

function sendToXmotor(ptzcmd, xpos=0,  ypos=0, xStep=0, yStep=0, speed=5){
    //takes ptz detail and builds async fetch request etc, defaults values to 0 if not passed in
    
    console.log ("Function vars are ");
    console.log (ptzcmd);
    console.log (xpos);
    console.log (ypos);
    console.log (speed);
    console.log (xStep);
    console.log (yStep);

    //setup connection to the server trying to use newer fetch function client side
    //Sent as Form data i.e. not POST as no need to encrypt in any way

    //create a form to send for simple positive steps e.g. up and right
      console.log ("creating form ");
      const formData = new FormData();

    //for everything we will use goto x,y and keep track of camera x,y 
    //camX, camY, maxX, maxY
    //xPos and yPos are global variables checking minX maxX and Y bounds etc

    //firstly is it a goto command in which case just bounds check as no step values
    console.log("checking ptzcmd parameters");

    //for now just trapping anything that isn't goto
    //take this out when completed to simplify 
    if (ptzcmd == "ptzinit" || ptzcmd == "ptzstatus" || ptzcmd == "ptzst"){
        console.log ("Cam status / initial setup / stop");
        
        formData.append('ptzcmd', ptzcmd);
        formData.append('xpos', xPos); //dont need these ??
        formData.append('ypos', yPos); //dont need these ??
        formData.append('speed', speed); //dont need these ??
    }   
    else if (ptzcmd=="ptzgoto") {
        formData.append('ptzcmd', ptzcmd);

        //test against maxXY
        CalcXandY(xpos, ypos);

        if (xPos!=xpos){ //if value corrected to camera min/max update text box
          document.getElementById('xpos').value=xPos;
        }
        formData.append('xpos', xPos);
        
        if (yPos!=ypos){
           //update on screen 
          document.getElementById('ypos').value=yPos;
        }
        formData.append('ypos', yPos);
        formData.append('speed', speed);
    }
    else {
        //all directions are using goto on camera

        //calculate x and y values
        CalcXandY(xpos, ypos, xStep, yStep);

        formData.append('ptzcmd', 'ptzgoto');
        formData.append('xpos', xPos);
        formData.append('ypos', yPos);
        formData.append('speed', speed);
        console.log ("New step to values are ");
        console.log ("ptzgoto for ", ptzcmd);
        console.log (xPos);
        console.log (yPos);
    }

    //send as a URL encoded string as nothing sensitive like passwords
    const payload = new URLSearchParams(formData);
  
    console.log("Payload is ");
    console.log (payload);

    //fire off async query     ** TO DO MAKE THIS A VARIABLE **
    fetch("/cgi-bin/ptz-xm530-cmd.cgi", {
      method: "POST",
      body: payload,
    })
    .then(res => res.json())
    .then(data => {
    
     console.log("got fetch respnse %s",data);

     //keep track of camera position
      camX=data.xpos;
      camY=data.ypos;
      status=data.status;
      
      if (status==65535){
          statustxt="idle";
      }
      else{
        statustxt="moving";
      }

      //set the values on screen now we have the response
      document.getElementById('ptzstatus').innerHTML=statustxt;

      if (status!=65535) {
        checkStatus();
      }
    })
    .catch(err => console.log(err));

}

//$ is defined in main.js shorthand for document.querySelector(n)

$("#speed")?.addEventListener("input", event => {
    console.log("This is slider input event");
    event.preventDefault(); //don't do standard html event e.g. submit form or follow href action.

    //changing the slider gives a value of between 1 and 10
    //for speed (when panning) we simply use that value
    //for single steps we multiply by 10;

    speed=document.getElementById('speed').value;
    console.log("speed is %d", speed);
    steps=speed*25;
    console.log("steps is %d", steps);

    //steps value is used in on click event of arrows
})


function testHeldDown(x,y){
    <!-- all buttons use goto x,y function -->
    event.preventDefault(); //don't do standard html event e.g. submit form or follow href action.
    console.log("mouse down event");
    //reset bool for mouseup has happened
    mymouseup=false;
    buttonhelddown=false;
    //start a timer here which if there hasn't
    // been a mousup yet will indicate we are holding the button down ?
    
    //just wait 1 seconds
    setTimeout(()=>{
        //this should run after 1000ms
        console.log("message after 1000ms delay using setTimeout()");
        
        //just catch that mouseup may have just happened
        if (mymouseup==false){
          console.log ("Button held down and no mouseup yet assuming long click");
          buttonhelddown=true;
          //setup goto maxX and/or maxY
           console.log("Sending goto message");
          console.log("x and y are %d %d speed=%d", x, y, speed);
          sendToXmotor('ptzgoto',x,y,speed);
          //send command now
        }
    }, 1000);

}

function ptzMouseUp(ptzcmd, xpos, ypos, xsteps, ysteps, speed ){
    <!-- all buttons use goto x,y function -->
    event.preventDefault(); //don't do standard html event e.g. submit form or follow href action.
    console.log("mouse up event");
    mymouseup=true;
    
    //need to test here if mousedown was held down and stop current goto maxX, maxy
    if (buttonhelddown==true){
      console.log("stopping movement");
      //send stop command
      sendToXmotor('ptzst');

    } else {
      //or this was a click event in which case it is a simple step
      console.log("Was a click event");
      sendToXmotor('ptzsul',camX,camY,xsteps,ysteps,speed);
    }
    buttonhelddown=false;
}

//up
$("#ptzsu")?.addEventListener("mousedown", event => {
    testHeldDown(xPos,yPos); //pass max / min param in required direction to pan to
    //console.log ("end of mousedown event");
})
$("#ptzsu")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsul',xPos,yPos,0,-steps,speed);
})

//up left
$("#ptzsul")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(0,0); 
})
$("#ptzsul")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsul',xPos,yPos,-steps,-steps,speed);
})
//up right
$("#ptzsur")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(maxX,0); 
})
$("#ptzsur")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsur',xPos,yPos,steps,-steps,speed);
})
//left
$("#ptzsl")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(0,yPos); 
})
$("#ptzsl")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsl',xPos,yPos,-steps,0 ,speed);
})
//right
$("#ptzsr")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(maxX,yPos); 
})
$("#ptzsr")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsr',xPos,yPos,steps,0 ,speed);
})
//down left
$("#ptzsdl")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(0,maxY); 
})
$("#ptzsdl")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsdl',xPos,yPos,-steps,steps ,speed);
})
//down
$("#ptzsd")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(xPos,maxY); 
})
$("#ptzsd")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsd',xPos,yPos,0,steps ,speed);
})
//down right
$("#ptzsdr")?.addEventListener("mousedown", event => {
    <!-- now need to send direction details etc to km-motor function -->
    testHeldDown(maxX,maxY); 
})
$("#ptzsdr")?.addEventListener("mouseup", event => {
    //use mouseup event instead of click event to allow monitoring for holding down button
    // so we can test for mousebutton being held down and pan in that direction
    ptzMouseUp('ptzsd',xPos,yPos,steps,steps ,speed);
})
//stop
$("#ptzst")?.addEventListener("click", event => {
    <!-- now need to send direction details etc to km-motor function -->
    event.preventDefault();
    sendToXmotor('ptzst');
})
//goto
$("#ptzgoto")?.addEventListener("click", event => {
    <!-- now need to send direction details etc to km-motor function -->
    event.preventDefault(); //don't do standard html event e.g. submit form or follow href action.
    //get x val
    x=document.getElementById('xpos').value
    //get y val
    y=document.getElementById('ypos').value
    console.log("Using speed value of ", speed)
    sendToXmotor('ptzgoto',x,y,0,0,speed);
})

</script>