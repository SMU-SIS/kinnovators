<%-- 
    Document   : register
    Created on : Nov 5, 2012, 2:02:33 AM
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
        
		<script type="text/javascript">
			 
		function CheckPassword(password)
		{
			var strength = new Array();
			strength[0] = "Blank";
			strength[1] = "Very Weak";
			strength[2] = "Weak";
			strength[3] = "Medium";
			strength[4] = "Strong";
			strength[5] = "Very Strong";
		
			var score = 1;
		
			if (password.length < 1)
				return strength[0];
		
			if (password.length < 4)
				return strength[1];
		
			if (password.length >= 8)
				score++;
			if (password.length >= 10)
				score++;
			if (password.match(/\d+/))
				score++;
			if (password.match(/[a-z]/) &&
				password.match(/[A-Z]/))
				score++;
			if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]/))
				score++;
		
			return strength[score];
		}
				
			function PasswordChanged(field)
			{
				var span = document.getElementById("PasswordStrength");
				span.innerHTML = CheckPassword(field.value);
			}
		
			function ButtonClicked(field)
			{
				var strength = document.getElementById("PasswordStrength").innerHTML;
				
				if (strength.indexOf("Strong") < 0)
				{
					alert("Password is not strong enough!");
					return false;
				}
			}
		</script>        
    </head>

    <body>

        <div class="span9">
            <div style="align:center" class="container-fluid">
            <% 
            	String error = (String) session.getAttribute("error");
            	if (error != null) {
            %>	
			<div class="alert alert-error">
				<a class="close">×</a>
				<%=error%>
			</div>
            <%
            		session.removeAttribute("error");
            	}
            %>
            	<h1 align="left">Registration</h1>
	            <form name="register" method="post" class="form-horizontal well" action="/RegisterServlet">
					<div class="control-group">
						<label class="control-label" for="inputUsername">Username</label>
						<div class="controls">
							<input type="text" id="inputUsername" placeholder="Username" name="username" >
						</div>
					</div>
					<div class="control-group">
						<label class="control-label" for="inputPassword">Password</label>
						<div class="controls">
							<input type="password" id="inputPassword" placeholder="Password" name="password"/>
						</div>
					</div>
					<div class="control-group">
						<label class="control-label" for="confirmPassword">Confirm Password</label>
						<div class="controls">
							<input type="password" id="confirmPassword" placeholder="Confirm Password" name="confirmpassword""/>							
						</div>
					</div>
					<div class="control-group">
						<label class="control-label" for="inputEmail">Email</label>
						<div class="controls">
							<input type="text" id="inputEmail" placeholder="Email" name="email" >
						</div>
					</div>				
					<div class="control-group">
						<label class="control-label" for="altLogin"> </label>
						<div class="controls"></div>
	 					<a href="#"><div class="fb-login-button" data-show-faces="false" data-width="200" data-max-rows="1"></div></a>
	                    <a href="#"><img src="images/goog-login-button.png"></img></a>
					</div>
					<div class="control-group">
						<div class="controls">
							<input type="submit" class="btn" value="Sign Me Up!">
						</div>
					</div>			
				</form>
            </div>
        </div>

    </body>
</html>
