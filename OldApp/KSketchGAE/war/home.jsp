<%-- 
    Document   : sketchpad
    Created on : Nov 4, 2012, 12:09:54 PM
    Author     : kwgoh.2010
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<jsp:include page="nav.jsp" />
<html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1" />
        <meta http-equiv="Content-Style-Type" content="text/css" />

        <title>
            K-Sketch: The Sketch Pad
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
    </head>

    <body>

        <div class="span9">
            <div class="container">
	            <% 
	            	String success = (String) session.getAttribute("success");
	            	String error = (String) session.getAttribute("error");
	            	if (error != null) {
	            %>	
				<div class="alert alert-error">
					<a class="close">×</a>
					<%=error%>
				</div>
	            <%
	            		session.removeAttribute("error");
	            	} else if (success != null) {
   	            %>	
   				<div class="alert alert-success">
   					<a class="close">×</a>
   					<%=success%>
   				</div>
   	            <%
   	            		session.removeAttribute("success");
   	            	}
            	%>
                <h1 align="left">Welcome to K-Sketch!</h1>

                <div class="row-fluid">
                    <div class="span4">
                        <iframe width="300" height="195" src="http://www.youtube.com/embed/UYLR5Nf4mWs" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <div class="span8">
                        <h3 align="left">About K-Sketch</h3>
                        <p align="left">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis consequat tristique leo sit amet sodales. Nam dapibus velit sed lorem tristique congue. In hac habitasse platea dictumst. Fusce nunc tortor, porta sed tempor ut, tincidunt id tortor. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin lobortis dignissim lectus, et iaculis velit porta sit amet. </p>                    
                    </div>
                </div>
                <div class="row-fluid">
                    <h3 align="left">K-Sketch Developers</h3>
                    <p align="left">Proin vehicula metus lorem. Nunc in luctus enim. Etiam at neque nunc, et lacinia dui. Praesent suscipit, mauris sed elementum porta, mauris tortor cursus elit, at tincidunt nulla justo eget massa. Vestibulum dolor est, rhoncus nec iaculis eget, rutrum vel sem. Donec urna augue, aliquam sit amet dignissim eu, fermentum at mauris. Sed vestibulum mauris eu mauris blandit suscipit. Mauris sed est nisi, quis blandit libero. </p>                    
                </div>
                <div class="row-fluid">
                    <h3 align="left">The Kinnovators!</h3>
                    <p align="left">Duis ac odio justo, sit amet tristique odio. Duis risus lorem, dictum vel tincidunt non, rutrum quis enim. Vivamus purus massa, scelerisque placerat iaculis quis, convallis a nibh. Etiam in lacinia elit. Pellentesque augue neque, ornare et venenatis ut, semper quis nulla. Fusce molestie rhoncus eros, vel venenatis eros porttitor a. </p>                    
                </div>
            </div>
            <div class="container">
                <h3 align="left">Most Popular Sketches</h3>
            </div>
        </div>

    </body>
</html>
