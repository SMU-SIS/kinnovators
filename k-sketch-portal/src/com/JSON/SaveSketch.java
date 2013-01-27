package com.JSON;

import com.model.Sketch;
import com.DAO.SketchDAO;

import java.util.ArrayList;
import java.util.Date;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class SaveSketch
 */

public class SaveSketch extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

	}
	
    /**
     * @see HttpServlet#HttpServlet()
     */
    public SaveSketch() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		processRequest(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    		response.setContentType("text/html;charset=UTF-8");
    		PrintWriter out = response.getWriter();
    		//DAO for Sketch objects
    		SketchDAO sketchDAO = new SketchDAO();
    		//New Sketch object
    		Sketch newSketch = null;
    		//JSONObject container
    		JSONObject obj = null;
    		
//    		//Input String for sketchName
//    		String sketchName = "";
//    		//Input String for sketchData
//    		String sketchData = "";
    		
    		try {
    			obj = new JSONObject(request.getParameter("sketch"));
    			//retrieve sketchName
    			String sketchName = obj.getString("sketchName");
    			//retrieve ownerId
    			Long ownerId = obj.getLong("ownerId");
    			//retrieve sketchData
    			String sketchData = obj.getString("sketchData");
    			//permissions do not exist yet - placeholder
    			ArrayList<String> permissions = new ArrayList<String>();
    			
    			//create newSketch
    			newSketch = new Sketch(sketchName, ownerId, new Date(), permissions, sketchData);
    			sketchDAO.addorUpdateSketch(newSketch);
    		} catch (JSONException e) {
    			//error
    		}
    }

}
