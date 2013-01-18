/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.servlets;

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
public class ActivateProfileServlet extends HttpServlet {

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

        int status = -1;

        String username = request.getParameter("profile").trim();
        System.out.println(username);
        if (username == null) {
            username = "";
        }        

        if (!username.trim().equals("")) {
        	status = userDAO.toggleActivation(username);
        }

        
        if (status == 1) {
            request.getSession().setAttribute("success", "You have successfully reactivated your account!");
            response.sendRedirect("editprofile.jsp?profile="+username);
            return;
        } else if (status == 0) {
            request.getSession().setAttribute("success", "You have successfully deactivated your account!");
            response.sendRedirect("editprofile.jsp?profile="+username);
            return;       	
        }
        
        request.getSession().setAttribute("error", "Error in activating/deactivating account. Please try again.");
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
