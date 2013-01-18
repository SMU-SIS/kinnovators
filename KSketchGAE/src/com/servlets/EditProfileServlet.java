/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.servlets;

import com.model.entity.User;
import com.model.DAO.UserDAO;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author kwgoh.2010
 */
@SuppressWarnings("serial")
public class EditProfileServlet extends HttpServlet {

    /**
     * Processes requests for both HTTP
     * <code>GET</code> and
     * <code>POST</code> methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();        
        UserDAO userDAO = new UserDAO();

        User user = null;

        String username = request.getParameter("username").trim();
        System.out.println(username);
        if (username == null) {
            username = "";
        }
        
        String password = request.getParameter("password").trim();
        System.out.println(password);
        if (password == null) {
            password = "";
        }
        
        String confirmpassword = request.getParameter("confirmpassword").trim();
        System.out.println(confirmpassword);
        if (confirmpassword == null) {
        	confirmpassword = "";
        }
        
        String email = request.getParameter("email").trim();
        System.out.println(email);
        if(email == null) {
    		email = "";
        }
        
        String firstname = request.getParameter("firstname").trim();
        System.out.println(firstname);
        if(firstname == null) {
    		firstname = "";
        }
        
        String lastname = request.getParameter("lastname").trim();
        System.out.println(lastname);
        if(lastname == null) {
        	lastname = "";
        }
        
        String description = request.getParameter("description");
        System.out.println(description);
        if(description == null) {
    		description = "";
        }

        if (password.trim().equals(confirmpassword.trim())) {
	        if (!username.trim().equals("") && !password.trim().equals("") && !email.trim().equals("")) {
	        	user = userDAO.update(username, password, email, firstname, lastname, description);
	        }
        }
        
        if (user != null) {
            request.getSession().setAttribute("success", "You have successfully updated your profile!");
            response.sendRedirect("editprofile.jsp?profile="+username);
            return;
        }
        
        request.getSession().setAttribute("error", "Error in updating profile. Please try again.");
        response.sendRedirect("editprofile.jsp?profile="+username);
        return;
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP
     * <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP
     * <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>
}
