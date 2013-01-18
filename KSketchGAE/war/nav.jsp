<%-- 
    Document   : nav
    Created on : Nov 4, 2012, 11:04:38 AM
    Author     : kwgoh.2010
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ page import="com.model.entity.User"%>
<style type="text/css">

    @import url("css/bootstrap.min.css");
    @import url("css/docs.css");
</style>
<script src="js/jquery-1.8.2.js"></script>
<script src="js/bootstrap.js"></script>

<html>
    <body class="preview" data-spy="scroll" data-target=".subnav" data-offset="80">
        <div id="fb-root"></div>
        <script>
            // Additional JS functions here
            window.fbAsyncInit = function() {
                FB.init({
                    appId      : '218710874927957', // App ID
                    //channelUrl : '//http://ksketch.ap01.aws.af.cm/sketchpad.jsp', // Channel File
                    channelUrl : '//http://ksketch.windchester.cloudbees.net/home.jsp', // Channel File
                    status     : true, // check login status
                    cookie     : true, // enable cookies to allow the server to access the session
                    xfbml      : true  // parse XFBML
                });
			
                function login() {
                    FB.login(function(response) {
                        if (response.authResponse) {
                            // connected
                            testAPI();
                        } else {
                            // cancelled
                        }
                    });
                }
                function testAPI() {
                    console.log('Welcome!  Fetching your information.... ');
                    FB.api('/me', function(response) {
                        console.log('Good to see you, ' + response.name + '.');
                    });
                }
                // Additional init code here
                FB.getLoginStatus(function(response) {
                    if (response.status === 'connected') {
                        // connected
                    } else if (response.status === 'not_authorized') {
                        // not_authorized
                        login();
                    } else {
                        // not_logged_in
                        login();
                    }
                });
        
            };
        
            // Load the SDK Asynchronously
            (function(d, s, id) {
                var js, fjs = d.getElementsByTagName(s)[0];
                if (d.getElementById(id)) return;
                js = d.createElement(s); js.id = id;
                js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=218710874927957";
                fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));
			
            /*(function(d){
     var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement('script'); js.id = id; js.async = true;
     js.src = "//connect.facebook.net/en_US/all.js";
                 218710874927957
     ref.parentNode.insertBefore(js, ref);
   }(document));*/
        </script>

        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container" style="width:90%">
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>
                    <a class="brand pull-left" href="home.jsp">K-Sketch</a>
                    <div class="nav-collapse" id="main-menu">
                        <% User user = (User) session.getAttribute("user");
                            if (user == null) {

                        %>
                        <form name="login" method="post" class="navbar-search pull-left" action="/LoginServlet">
                            <input type="text" class="search-query span2" id="username" name="username" placeholder="Username">
                            <input type="password" class="search-query span2" id="password" name="password" placeholder="Password">
                            <input type="submit" class="button btn-info" value="Login">
                        </form>
                        <ul class="nav">
                            <li class="dropdown">
                                <a data-toggle="dropdown" class="dropdown-toggle" href="#"><b class="caret"></b></a>
                                <ul class="dropdown-menu">
                                    <li><a href="register.jsp">Register</a></li>
                                    <li><a href="#ForgotPassword" data-toggle="modal">Forgot Password</a></li>
                                </ul>
                            </li>
                            <li><a href="#"><div class="fb-login-button" data-show-faces="false" data-width="200" data-max-rows="1"></div></a></li>
                            <li><a href="#"><img src="images/goog-login-button.png"></img></a></li>
                        </ul>
                        <%                        
                            } else {
                        %>
                            <ul class="nav">
                                <li><a href="sketchbook.jsp?profile=<%=user.getUsername() %>">Hi, <%=user.getUsername()%>!</a></li>
                                <li><a href="/LogoutServlet">Logout</a></li>
                            </ul>
                        <% 
                            }
                        %>
                    </div> 
                    <div class="nav-collapse pull-right" id="main-menu">

                        <form name="search" class="navbar-search pull-right" method="post" action="">
                            <input type="text" class="search-query span4" id="search" name="search" placeholder="Search">
                            <input type="submit" class="button btn-info" value=">">
                        </form>
                    </div> 
                </div>
            </div>
        </div>
        <br/>
        <br/>
        <br/>
        <div class="span3 bs-docs-sidebar">
            <ul class="nav nav-tabs nav-stacked">
            	<% if (user == null) { %>
	                <li><a href="#"><i class="icon-chevron-right"></i> Sketchbook</a>
	                </li>
                <% } else { %>
	                <li><a href="sketchbook.jsp?profile=<%=user.getUsername() %>"><i class="icon-chevron-right"></i> Sketchbook</a>
	                </li>                
                <% } %>
                <li><a href="sketchpad.jsp"><i class="icon-chevron-right"></i> Create a Sketch</a>
                </li>
                <li><a href="sketchpad.jsp"><i class="icon-chevron-right"></i> View a Sketch</a>
                </li>
            </ul>
        </div>
        
        <!--Registration Modal-->
		<div class="modal hide fade" id="ForgotPassword" tabindex="-1" role="dialog"
			aria-labelledby="myForgotPassword" aria-hidden="true">
			<div class="modal-header">
				<h3 id="myForgotPassword">Forgot Your Password?</h3>
			</div>
			<div class="modal-body">
				<form name="signin" method="post" class="form-horizontal" action="/ForgotPasswordServlet">
					<p>No worries. Enter the email address of your account below, and we will send you your password!</p>
					<div class="control-group">
						<label class="control-label" for="inputPassword">Email Address</label>
						<div class="controls">
							<input type="text" id="inputemail" placeholder="Email Address" name="email">
						</div>
					</div>
					<div class="control-group">
							<button type="button" class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>
							<input type="submit" value="Confirm" class="btn">
					</div>
				</form>
			</div>
			<div class="modal-footer"></div>
		</div>
    </body>
</html>
