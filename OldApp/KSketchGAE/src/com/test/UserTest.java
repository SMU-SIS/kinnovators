/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.test;

import com.model.DAO.UserDAO;
import com.model.entity.User;

import javax.naming.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author kwgoh.2010 
 */
@SuppressWarnings("serial")
public class UserTest extends HttpServlet {

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
        ArrayList<User> list = (ArrayList<User>) userDAO.retrieveAll();
        
        out.println("<table border='1'>");
    	out.println("<thead>");
    	out.println("<tr>");
    	out.println("<td>id</td>");
    	out.println("<td>username</td>");
    	out.println("<td>password</td>");
    	out.println("<td>email</td>");
    	out.println("<td>facebookEmail</td>");
    	out.println("<td>googlePlusEmail</td>");
    	out.println("<td>registeredDate</td>");
    	out.println("<td>appVersion</td>");
    	out.println("<td>firstName</td>");
    	out.println("<td>lastName</td>");
    	out.println("<td>description</td>");
    	out.println("<td>active</td>");
    	out.println("</tr>");
    	out.println("</thead>");
    	out.println("<tbody>");
        for (int i = 0; i < list.size(); i++) {
        	User user = list.get(i);
        	out.println("<tr>");
        	out.println("<td>" + user.getID() + "</td>");
        	out.println("<td>" + user.getUsername() + "</td>");
        	out.println("<td>" + user.getPassword() + "</td>");
        	out.println("<td>" + user.getEmail() + "</td>");
        	out.println("<td>" + user.getFacebookEmail() + "</td>");
        	out.println("<td>" + user.getGooglePlusEmail() + "</td>");
        	out.println("<td>" + user.getRegisteredDate() + "</td>");
        	out.println("<td>" + user.getAppVersion() + "</td>");
        	out.println("<td>" + user.getFirstname() + "</td>");
        	out.println("<td>" + user.getLastname() + "</td>");
        	out.println("<td>" + user.getDescription() + "</td>");
        	out.println("<td>" + user.isActive() + "</td>");
        	out.println("</tr>");
        }
        out.println("</tbody>");
        out.println("</table>");
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
