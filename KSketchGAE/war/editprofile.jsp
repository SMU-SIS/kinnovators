<%-- 
    Document   : sketchpad
    Created on : Nov 4, 2012, 12:09:54 PM
    Author     : kwgoh.2010
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page import="com.model.entity.User, com.model.DAO.UserDAO, java.util.*"%>
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
    </head>

    <body>
		<% 
			UserDAO userDAO = new UserDAO();
			String profile = request.getParameter("profile").trim();
			if (profile == null) {
				response.sendRedirect("home.jsp");
				return;
			} else if (profile.trim().equals("")) {
				response.sendRedirect("home.jsp");
				return;
			}
			User profileUser = userDAO.retrieve(profile);
			if (profileUser == null) {
				response.sendRedirect("home.jsp");
				return;
			}
			User currentUser = (User) session.getAttribute("user");
			String current = "";
			if (currentUser != null) {
				current = currentUser.getUsername().toLowerCase();
			}
			if (!current.trim().equals(profile.toLowerCase())) {
				session.setAttribute("error", "You may only edit your own profile!");
				response.sendRedirect("sketchbook.jsp?profile="+profile.toLowerCase());
				return;
			}
		%>
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
				<div class="span9">
					<h2 align="left">Editing My Profile</h2>
				</div>
				<div class="row-fluid">
					<div class="span9">
						<form name="register" method="post" class="form-horizontal well" action="/EditProfileServlet">
							<div class="control-group">
								<label class="control-label" for="inputUsername">Username</label>
								<div class="controls">
									<%=profileUser.getUsername() %>
									<input type="hidden" id="inputUsername" value="<%=profileUser.getUsername() %>" name="username" >
								</div>
							</div>
							<div class="control-group">
								<label class="control-label" for="inputPassword">Password</label>
								<div class="controls">
									<input type="password" id="inputPassword" value="<%=profileUser.getPassword() %>" name="password"/>
								</div>
							</div>
							<div class="control-group">
								<label class="control-label" for="confirmPassword">Confirm Password</label>
								<div class="controls">
									<input type="password" id="confirmPassword" value="<%=profileUser.getPassword() %>" name="confirmpassword""/>							
								</div>
							</div>
							<div class="control-group">
								<label class="control-label" for="inputEmail">Email</label>
								<div class="controls">
									<input type="text" id="inputEmail" value="<%=profileUser.getEmail() %>" name="email" >
								</div>
							</div>				
							<div class="control-group">
								<label class="control-label" for="inputFirstname">First Name</label>
								<div class="controls"></div>
			 						<input type="text" id="inputFirstname" value="<%=profileUser.getFirstname() %>" name="firstname" >
							</div>
							<div class="control-group">
								<label class="control-label" for="inputLastname">Last Name</label>
								<div class="controls"></div>
			 						<input type="text" id="inputLastname" value="<%=profileUser.getLastname() %>" name="lastname" >
							</div>
							<div class="control-group">
								<label class="control-label" for="inputDescription">Description</label>
								<div class="controls"></div>
			 						<textarea id="inputDescription" class="input-xlarge" rows "3" name="description" ><%=profileUser.getDescription() %></textarea>
							</div>							
							<div class="control-group">
								<div class="controls">
									<input type="submit" class="btn" value="Save Changes">
								</div>
							</div>			
						</form>
          			</div>				
					<div class="span2 offset 1">
						<div class="row-fluid">
							<div class="img-polaroid img-polaroid-crop">
	          					<div class="img-crop">
	          						<img src="images/users/anonymous.jpg"></img>
	          					</div>
	          				</div>
	          			</div>
	          			<div class="row-fluid">
          					<a class="btn btn-small" href="#">Change Profile Picture</a>
          				</div>
          				<div class="row-fluid">
          					<br/>
          					<br/>
          					<% if (profileUser.isActive()) { %>
          					<p align="left">Account Status: Active</p>
          					<br/>
          					<br/>
          					<a class="btn btn-info" href="/ActivateProfileServlet?profile=<%=profileUser.getUsername() %>">Deactivate My Account</a>
          					<% } else { %>
          					<p align="left">Account Status: Inactive</p>
          					<br/>
          					<br/>
          					<a class="btn btn-info" href="/ActivateProfileServlet?profile=<%=profileUser.getUsername() %>">Reactivate My Account</a>
          					<% } %>
						</div>
          			</div>
				</div>
			</div>       
        </div>

    </body>
</html>
