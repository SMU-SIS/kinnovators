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
		%>
        <div class="span9">
			<div class="container">
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
				<div class="row">
					<div class="span9">
						<% if (current.trim().equals(profile.trim().toLowerCase())) { %>
						<h2 align="left">About Me</h2>
						<% } else {  %>
						<h2 align="left">About <%=profile %></h2>
						<% }  %>
					</div>
					<div class="span3">
						<% if (current.trim().equals(profile.trim().toLowerCase())) { %>
						<a class="btn btn-info pull-left" href="editprofile.jsp?profile=<%=profile %>">Edit Profile</a>
						<% }  %>
					</div>
				</div>
				<div class="row-fluid">
					<div class="span2">
						<div class="img-polaroid img-polaroid-crop">
          					<div class="img-crop">
          						<img src="images/users/anonymous.jpg"></img>
          					</div>
          				</div>
          			</div>				
					<div class="span9 offset 1">
						<p align="left">
							<b>Name:</b> <%=profileUser.getFirstname() %> <%=profileUser.getLastname() %>
						</p>
						<p align="left">
							<b>Date Registered:</b> <%=profileUser.getRegisteredDate().toString() %>
						</p>
						<p align="left">
							<b>Description:</b> <%=profileUser.getDescription() %>
						</p>
						<p align="left">
							<% if (current.trim().equals(profile.trim().toLowerCase())) {
									if (profileUser.isActive()) {%>
								Your account is active.
							<% 		} else { %>
								Your account is inactive.
							<%		}
								} else {  
									if (!profileUser.isActive()) { %>
								This user has deactivated their account.								
							<% 		} 
								}  %>
						</p>
					</div>
				</div>
			</div>
			<hr/>
			<div class="container">
				<div class="row">
					<div class="span9">
						<% if (current.trim().equals(profile.trim().toLowerCase())) { %>
						<h3 align="left">My Sketches</h3>
						<% } else {  %>
						<h3 align="left"><%=profile %>'s Sketches</h3>
						<% }  %>
					</div>
					<div class="span3">
						<div class="pagination">
					        <ul>
					          <li><a href="#">←</a></li>
					          <li class="disabled"><a href="#">1</a></li>
					          <li class="active"><a href="#">2</a></li>
					          <li><a href="#">3</a></li>
					          <li><a href="#">→</a></li>
					        </ul>
					    </div>
					</div>
				</div>
				<div class="row"></div>
			</div>
			<hr/>
			<div class="container">
				<div class="row">
					<div class="span9">
						<% if (current.trim().equals(profile.trim().toLowerCase())) { %>
						<h3 align="left">Favourite Sketches</h3>
						<% } else {  %>
						<h3 align="left"><%=profile %>'s Favourite Sketches</h3>
						<% }  %>
					</div>
					<div class="span3">
						<div class="pagination">
					        <ul>
					          <li><a href="#">←</a></li>
					          <li class="disabled"><a href="#">1</a></li>
					          <li class="active"><a href="#">2</a></li>
					          <li><a href="#">3</a></li>
					          <li><a href="#">→</a></li>
					        </ul>
					    </div>
					</div>
				</div>
				<div class="row"></div>			
			</div>           
        </div>

    </body>
</html>
