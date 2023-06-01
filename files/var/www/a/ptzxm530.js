//This is the script to support ptz in preview.cgi
//use on page load event to get the currrent x,y vals from the camera
//initially in case that fails, camera could be off etc then fill with 0,0
//could set these in the form but here ensures always reset to a value.
 
//The sendToXmotor function below returns a json string including status, xpos,ypos
//so we will use that to capture the current camera position on page load

//global vars 
//vars to track cam x,y
let camX=0; 
let camY=0;
let maxX=0;
let maxY=0;
let camstatus=0;
let steps=100; //seems a good value for each click of the direction buttons
let speed=5; //options 1-10 
let mymouseup=false;
let xPos=0; //form values i.e. client side x and y 
let yPos=0;

//Var to hold specific camera script required to translate generic up, down, left, right etc..
//The idea is for a generic UI and 'simple' swap of the script to handle the conversions required for different cameras
const ptzcgi = "/cgi-bin/ptzxm530cmd.cgi"

//runs on initial page load from eventlistener to ensure form elements exist
window.addEventListener('load', (event) => {
//we could double check on page load that the kmotor module is loaded however 
//it fails relatively safely with incorrect x and y values. Could use an async query to get 
//result of ps or check modules file for required entry.

//set the default x,y params on screen
document.getElementById('xpos').value=camX;
document.getElementById('ypos').value=camY;

//contact the camera to pull off the max X and max Y params using -i option in updated xm-kmotor
const formData = new FormData();
formData.append('ptzcmd', "ptzinit");

//ensure gets sent as a URL encoded string as nothing sensitive like passwords
const payload = new URLSearchParams(formData);

//create async call ptzcmd===global var holding cam specific handler script.   
fetch(ptzcgi, {
  method: "POST",
  body: payload,
})
.then(res => res.json())
.then(data => {
  //console.log(data);

  //now keep the camera values to track for this session
  camX=data.xpos;
  camY=data.ypos;
  maxX=data.xmax;
  maxY=data.ymax;
  camstatus=data.status; //65535 is when idle other values not known

  if (camstatus==65535){
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
const formData = new FormData();
formData.append('ptzcmd', "ptzstatus");

const payload = new URLSearchParams(formData);

let loopcount=0;
//start of loop to get camera status 
do {
//repeat check cam status every 1/2 second 
//wait 11/2 second and try again
await waitms(500);

//console\.log("getting status");
//create async call ptzcmd===global var holding cam specific handler script. 
fetch(ptzcgi, {
  method: "POST",
  body: payload,
})
.then(res => res.json())
.then(data => {

camX=data.xpos;
camY=data.ypos;
camstatus=data.status;
//console\.log("status - %s", camstatus);

if (camstatus==65535){ 
   statustxt="idle";
}
else{
  statustxt="moving";
}
//console\.log("statustxt - %s", statustxt);
document.getElementById('ptzstatus').innerHTML=statustxt;
document.getElementById('camCurrentX').innerHTML=camX;
document.getElementById('camCurrentY').innerHTML=camY;

  })
  
    loopcount++;
    //do this for the max number of seconds to move from 0 to max x and y 
    //just needs to be slightly longer than time for camera to travel 0-max x or y axis.
    //console.log("statustxt - %s", statustxt);

    //** TODO make it configurable (speed setting 1-10 multiplied by time per step or something similar)

  } while (camstatus<65535&&loopcount<60);
}

function CalcXandY(x,y,xStep=0,yStep=0){ //pass in +x +y vals test against maxX, maxY and 0

//console.log ("calc x & y start");
//console.log ("x is ", x);
//console.log ("y is ", y);
//console.log ("xStep is ", xStep);
//console.log ("yStep is ", yStep);
//console.log ("xPos is ", xPos);
//console.log ("ypos is ", yPos);

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

//console.log ("calc x & y end");
//console.log ("x is ", x);
//console.log ("y is ", y);
//console.log ("xPos is ", xPos);
///console.log ("ypos is ", yPos);

}

function sendToXmotor(ptzcmd, xpos=0,  ypos=0, xStep=0, yStep=0, speed=5){
//takes ptz detail and builds async fetch request etc, defaults values to 0 if not passed in

//setup connection to the server using newer fetch function client side

//create a form to send for simple positive steps e.g. up and right
const formData = new FormData();

//for everything we will use goto x,y and keep track of camera x,y 
//camX, camY, maxX, maxY
//xPos and yPos are global variables checking minX maxX and Y bounds etc

//firstly is it a goto command in which case just bounds check as no step values

if (ptzcmd == "ptzinit" || ptzcmd == "ptzstatus" || ptzcmd == "ptzst"){
    //console.log ("Cam status / initial setup / stop");
    
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
    //all directions are using goto function on camera

    //calculate x and y values
    CalcXandY(xpos, ypos, xStep, yStep);

    formData.append('ptzcmd', 'ptzgoto');
    formData.append('xpos', xPos);
    formData.append('ypos', yPos);
    formData.append('speed', speed);
    //console.log ("New step to values are ");
    //console.log ("ptzgoto for ", ptzcmd);
    //console.log (xPos);
    //console.log (yPos);
}

//send as a URL encoded string as nothing sensitive like passwords
const payload = new URLSearchParams(formData);

//console.log("Payload is ");
//console.log (payload);


//fire off async query
fetch(ptzcgi, {
  method: "POST",
  body: payload,
})
.then(res => res.json())
.then(data => {

 //keep track of camera position
  camX=data.xpos;
  camY=data.ypos;
  camstatus=data.status;
  
  if (camstatus==65535){
      statustxt="idle";
  }
  else{
    statustxt="moving";
  }

  //set the values on screen now we have the response
  document.getElementById('ptzstatus').innerHTML=statustxt;

  if (camstatus!=65535) {
    checkStatus();
  }
})
.catch(err => console.log(err));

}

//$ is defined in main.js shorthand for document.querySelector(n)

$("#speed")?.addEventListener("input", event => {

//changing the slider gives a value of between 1 and 10
//for speed (when panning) we simply use that value
//for single steps we multiply by 10;

speed=document.getElementById('speed').value;
steps=speed*25;
//steps value is used in on click event of arrows
})


function testHeldDown(x,y){
//all buttons use goto x,y function
//console.log("mouse down event");
//reset bool for mouseup has happened
mymouseup=false;
buttonhelddown=false;
//start a timer here which if there hasn't
// been a mousup yet will indicate we are holding the button down ?

//just wait 1 seconds
setTimeout(()=>{
    //this should run after 1000ms
    //console.log("message after 1000ms delay using setTimeout()");
    
    //just catch that mouseup may have just happened
    if (mymouseup==false){
      //console.log ("Button held down and no mouseup yet assuming long click");
      buttonhelddown=true;
      //setup goto maxX and/or maxY
      //console.log("Sending goto message");
      //console.log("x and y are %d %d speed=%d", x, y, speed);
      sendToXmotor('ptzgoto',x,y,speed);
      //send command now
    }
}, 1000);

}

function ptzMouseUp(ptzcmd, xpos, ypos, xsteps, ysteps, speed ){
// all buttons use goto x,y function 
//console.log("mouse up event");
mymouseup=true;

//need to test here if mousedown was held down and stop current goto maxX, maxy
if (buttonhelddown==true){
  //console.log("stopping movement");
  //send stop command
  sendToXmotor('ptzst');

} else {
  //or this was a click event in which case it is a simple step
  //console.log("Was a click event");
  sendToXmotor('ptzsul',camX,camY,xsteps,ysteps,speed);
}
buttonhelddown=false;
}

//up
$("#ptzsu")?.addEventListener("mousedown", event => {
//make the button looked pressed down

testHeldDown(xPos,yPos); //pass max / min param in required direction to pan to
//console.log ("end of mousedown event");
})
$("#ptzsu")?.addEventListener("mouseup", event => {
//restore the button image to not pressed down

//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsul',xPos,yPos,0,-steps,speed);
})

//up left
$("#ptzsul")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function 
testHeldDown(0,0); 
})
$("#ptzsul")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsul',xPos,yPos,-steps,-steps,speed);
})
//up right
$("#ptzsur")?.addEventListener("mousedown", event => {
//now need to send direction details etc to km-motor function -->
testHeldDown(maxX,0); 
})
$("#ptzsur")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsur',xPos,yPos,steps,-steps,speed);
})
//left
$("#ptzsl")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function
testHeldDown(0,yPos); 
})
$("#ptzsl")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsl',xPos,yPos,-steps,0 ,speed);
})
//right
$("#ptzsr")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function 
testHeldDown(maxX,yPos); 
})
$("#ptzsr")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsr',xPos,yPos,steps,0 ,speed);
})
//down left
$("#ptzsdl")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function
testHeldDown(0,maxY); 
})
$("#ptzsdl")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsdl',xPos,yPos,-steps,steps ,speed);
})
//down
$("#ptzsd")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function 
testHeldDown(xPos,maxY); 
})
$("#ptzsd")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsd',xPos,yPos,0,steps ,speed);
})
//down right
$("#ptzsdr")?.addEventListener("mousedown", event => {
// now need to send direction details etc to km-motor function
testHeldDown(maxX,maxY); 
})
$("#ptzsdr")?.addEventListener("mouseup", event => {
//use mouseup event instead of click event to allow monitoring for holding down button
// so we can test for mousebutton being held down and pan in that direction
ptzMouseUp('ptzsd',xPos,yPos,steps,steps ,speed);
})
//stop
$("#ptzst")?.addEventListener("click", event => {
// now need to send direction details etc to km-motor function
sendToXmotor('ptzst');
})
//goto
$("#ptzgoto")?.addEventListener("click", event => {
// now need to send direction details etc to km-motor function
//get x val
x=document.getElementById('xpos').value
//get y val
y=document.getElementById('ypos').value
//console.log("Using speed value of ", speed)
sendToXmotor('ptzgoto',x,y,0,0,speed);
})
