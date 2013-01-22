'use strict';

<% page import="com.google.appengine.api.users.*"; %>

/* Controllers */


function FirstController($scope) {
   <%
	 UserService userService = UserServiceFactory.getUserService();
     String username = (String) session.getAttribute("username");
    %>
   $scope.name = <% username; %>;
}

