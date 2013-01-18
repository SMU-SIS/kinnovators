<%-- 
    Document   : sketchpad
    Created on : Nov 4, 2012, 12:09:54 PM
    Author     : kwgoh.2010
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<jsp:include page="nav.jsp" />
<html ng-app xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1" />
        <meta http-equiv="Content-Style-Type" content="text/css" />

        <title>
            K-Sketch: The Kinetic Sketch Pad
        </title>


        <style type="text/css" media="screen"> 
            html, body  { height:100%; }
            body { margin:0; padding:0; overflow:auto; text-align:center; 
                   background-color: #ffffff; }   
            object:focus { outline:none; }
            #flashContent { display:none; }
        </style>
        <!-- Enable Browser History by replacing useBrowserHistory tokens with two hyphens -->
        <!-- BEGIN Browser History required section -->
        <link rel="stylesheet" type="text/css" href="history/history.css" />
        <script type="text/javascript" src="history/history.js"></script>
        <!-- END Browser History required section -->  

		<script src="http://code.angularjs.org/angular-1.0.0rc3.min.js"></script>
		<script src="http://documentcloud.github.com/underscore-min.js"></script>
        <script type="text/javascript" src="swfobject.js"></script>
                 <script type="text/javascript" src="KSketchCallBacks.js"></script>
        <script type="text/javascript">
            // For version detection, set to min. required Flash Player version, or 0 (or 0.0.0), for no version detection. 
            var swfVersionStr = "10.2.0";
            // To use express install, set to playerProductInstall.swf, otherwise the empty string. 
            var xiSwfUrlStr = "playerProductInstall.swf";
            var flashvars = {};
            var params = {};
            params.quality = "high";
            params.bgcolor = "#ffffff";
            params.allowscriptaccess = "sameDomain";
            params.allowfullscreen = "true";
            var attributes = {};
            attributes.id = "KSketch2_Web";
            attributes.name = "KSketch2_Web";
            attributes.align = "middle";
            swfobject.embedSWF(
            "KSketch2_Web.swf", "flashContent", 
            "922", "518", 
            swfVersionStr, xiSwfUrlStr, 
            flashvars, params, attributes);
            // JavaScript enabled so display the flashContent div in case it is not replaced with a swf object.
            swfobject.createCSS("#flashContent", "display:block;text-align:left;");
        </script>
    </head>

    <body>

        <div class="span9">
        	<div class="container">
	            <% 
	            	if (session.getAttribute("user") == null) {
	            %>	
				<div class="alert alert-info">
					<a class="close">×</a>
					You are not currently logged in to KSketch! You can still create a sketch, but you need to login to save it.
				</div>
	            <%
	            	} 
   	            %>
   	            <!-- Start of Main Content Area -->

                <div id="flashContent">
                    <p>
                        To view this page ensure that Adobe Flash Player version 
                        10.2.0 or greater is installed. 
                    </p>
                    <script type="text/javascript"> 
                        var pageHost = ((document.location.protocol == "https:") ? "https://" : "http://"); 
                        document.write("<a href='http://www.adobe.com/go/getflashplayer'><img src='" 
                            + pageHost + "www.adobe.com/images/shared/download_buttons/get_flash_player.gif' alt='Get Adobe Flash player' /></a>" ); 
                    </script> 
                </div>
                <noscript>
                    <object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="922" height="518" id="KSketch2_Web">
                        <param name="movie" value="KSketch2_Web.swf" />
                        <param name="quality" value="high" />
                        <param name="bgcolor" value="#ffffff" />
                        <param name="allowScriptAccess" value="sameDomain" />
                        <param name="allowFullScreen" value="true" />
                        <!--[if !IE]>-->
                        <object type="application/x-shockwave-flash" data="KSketch2_Web.swf" width="922" height="518">
                            <param name="quality" value="high" />
                            <param name="bgcolor" value="#ffffff" />
                            <param name="allowScriptAccess" value="sameDomain" />
                            <param name="allowFullScreen" value="true" />
                            <!--<![endif]-->
                            <!--[if gte IE 6]>-->
                            <p> 
                                Either scripts and active content are not permitted to run or Adobe Flash Player version
                                10.2.0 or greater is not installed.
                            </p>
                            <!--<![endif]-->
                            <a href="http://www.adobe.com/go/getflashplayer">
                                <img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="Get Adobe Flash Player" />
                            </a>
                            <!--[if !IE]>-->
                        </object>
                        <!--<![endif]-->
                    </object>
                </noscript>     
        	</div>
		</div>
    </body>
</html>
