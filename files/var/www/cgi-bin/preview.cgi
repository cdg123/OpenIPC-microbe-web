#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Camera preview & setup"

size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
size_w=${size%x*}
size_h=${size#*x}
%>

<%in p/header.cgi %>

<link rel="stylesheet" href="/a/ptz.css">

<div class="row preview">
  <div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">
    <% preview 1 %>
    <p class="small text-body-secondary">The image above refreshes once per second and may appear choppy.
    To see a smooth video feed from the camera use one of the <a href="majestic-endpoints.cgi" target="_blank">video endpoints</a>.
  </div>
  <div class="col-md-4 col-xl-3 col-xxl-3">
    <div class="d-grid gap-2 mb-3">
      <div class="input-group">
        <div class="input-group-text">
          <img src="/a/light-off.svg" alt="Image: Night mode indicator" id="night-mode-status">
        </div>
        <button class="form-control btn btn-primary text-start" type="button" id="toggle-night-mode">Toggle night mode</button>
        <div class="input-group-text">
          <a href="majestic-settings.cgi?tab=nightMode" title="Night mode settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="email">Send to email</button>
        <div class="input-group-text">
          <a href="plugin-send2email.cgi" title="Email settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="ftp">Send to FTP</button>
        <div class="input-group-text">
          <a href="plugin-send2ftp.cgi" title="FTP Storage settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="telegram">Send to Telegram</button>
        <div class="input-group-text">
          <a href="plugin-send2telegram.cgi" title="Telegram bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="mqtt">Send to MQTT</button>
        <div class="input-group-text">
          <a href="plugin-send2mqtt.cgi" title="MQTT settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="webhook">Send to webhook</button>
        <div class="input-group-text">
          <a href="plugin-send2webhook.cgi" title="Webhook settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="yadisk">Send to Yandex Disk</button>
        <div class="input-group-text">
          <a href="plugin-send2yadisk.cgi" title="Yandex Disk bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="openwall">Send to Open Wall</button>
        <div class="input-group-text">
          <a href="plugin-send2openwall.cgi" title="Open Wall settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>

      <% if [ "xm530" =  "$soc" ];
      then %> 
        <div>
        <div class="ptzcontainer2" id="ptzform">
          <div class="box"><img src="/a/ptzFaster.svg" alt="Faster"></div>
          <div class="box-borderright"></div>
          <div class="box-ptzcolumn ptzimages">
          
          <a href="#" title="Step Up Left" id="ptzsul"><img class="hoverclick" src="/a/ptzUpLeft.svg" alt="Step Up Left"></a>
          <a href="#" title="Step Up" id="ptzsu"><img class="hoverclick" src="/a/ptzUp.svg" alt="Step Up"></a>
          <a href="#" title="Step Up Right" id="ptzsur"><img class="hoverclick" src="/a/ptzUpRight.svg" alt="Step Up Right"></a>
        <br>
        <a href="#" title="Step Left" id="ptzsl"><img class="hoverclick" src="/a/ptzLeft.svg" alt="Step Left"></a>
          <a href="#" title="Stop" id="ptzst"><img class="hoverclick" src="/a/ptzStop.svg" alt="Stop"></a>
          <a href="#" title="Step Right" id="ptzsr"><img class="hoverclick" src="/a/ptzRight.svg" alt="Step Right"></a>
        <br>  
          <a href="#" title="Step Down Left" id="ptzsdl"><img class="hoverclick" src="/a/ptzDownLeft.svg" alt="Step Down Left"></a>
          <a href="#" title="Step Down" id="ptzsd"><img class="hoverclick" src="/a/ptzDown.svg" alt="Step Down"></a>
          <a href="#" title="Step Down Right" id="ptzsdr"><img class="hoverclick" src="/a/ptzDownRight.svg" alt="Step Down Right"></a>
        </div>

        <!-- X here ***** -->
          <div class="box-borderleftrightbottom linesmall ptzXyText">X<br><input type="text" class="ptzTextbox" id="xpos" name="ptzxpos" tabindex="1">
             </div>
            <div>
        </div>

          <div class="verticaltext x-small">speed</div>
          <div class="box-borderright">
          <div class="slider">
            <input type="range" min="1" max="10" value="5" step="1" id="speed" show="true">
            </div>
          </div>
          <!-- y here ***** -->
          <div class="box-borderleftrightbottom linesmall ptzXyText">Y<br><input type="text" class="ptzTextbox" id="ypos" name="ptzypos" tabindex="2"></div>
          <div></div>
          <div class="box-bottom"><img src="/a/ptzSlower.svg" alt="Slower"></div>
            <div class="box-borderright"></div>

          <div class="box-borderleftright"><input class="hoverclick" type="image" value="goto" id="ptzgoto" name="goto x,y" alt="go" src="/a/ptzGoto.svg" tabindex="3"></div>
          <div class="box"></div>
          <div class="box"></div>
          <div class="box-middle x-small" id="speed-show">5</div>
          <div class="box-bordertop x-small">x:<div class="status" id="camCurrentX" name="camCurrentX">123456</div>&nbsp;y:<div class="status" id="camCurrentY" name="camCurrentY">1234</div></div>
          <div class="box-ptzstatus box-bordertop x-small">status:<div class="status" id="ptzstatus" name="ptzstatus">moving</div></div>
          
        </div>
        <p>Click and hold buttons to pan<br />
        <br />
        For live stream with overlay controls goto <A href="#" ptzoverlay.cgi>the overlay page</a>
        </p>
        </div>
      <% else %>
        "Sorry ptz features not avialable for your camera model yet"      
      <% fi %> 
          
          <div><hr class="dropdown-divider"></div>
    </div>

  <!-- this is end of right hand column -->
  </div>
</div>

<script>
const network_address = "<%= $network_address %>";

<% [ "true" != "$email_enabled"    ] && echo "\$('button[data-sendto=email]').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('button[data-sendto=ftp]').disabled = true;" %>
<% [ "true" != "$mqtt_enabled"     ] && echo "\$('button[data-sendto=mqtt]').disabled = true;" %>
<% [ "true" != "$webhook_enabled"  ] && echo "\$('button[data-sendto=webhook]').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('button[data-sendto=telegram]').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('button[data-sendto=yadisk]').disabled = true;" %>

function reqListener(data) {
  console.log(data.responseText);
}

$("#toggle-night-mode")?.addEventListener("click", event => {
  event.preventDefault();
  $('#night-mode-status').src = ($('#night-mode-status').src.split("/").pop() == "light-on.svg") ? "/a/light-off.svg" : "/a/light-on.svg";
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/cgi-bin/night.cgi");
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("mode=toggle");
});

$$("button[data-sendto]").forEach(el => el.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const tgt = event.target.dataset["sendto"];
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send.cgi?to=" + tgt);
    xhr.send();
}))
</script>

<script src="/a/ptzxm530.js"></script>

<%in p/footer.cgi %>
