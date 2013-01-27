package com.JSON;

import com.model.Sketch;
import com.DAO.SketchDAO;

import org.json.JSONObject;
import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class LoadSketch
 */

public class LoadSketch extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public LoadSketch() {
        super();
        // TODO Auto-generated constructor stub
    }

    protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

	}    
    
	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    		processRequest(request, response);
    }

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
    @SuppressWarnings("null")
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    		response.setContentType("text/html;charset=UTF-8");
    		PrintWriter out = response.getWriter();
    		//DAO for Sketch objects
    		SketchDAO sketchDAO = new SketchDAO();
    		//id of Sketch
    		Long id = 0L;
    		//Loaded Sketch object
    		Sketch loadSketch = null;
    		//JSON representation of Sketch
    		JSONObject loadSketchJSON = null;
    		
//    		//Input String for sketchName
//    		String sketchName = "";
//    		//Input String for sketchData
//    		String sketchData = "";
    		
    		try {
    			id = Long.parseLong(request.getParameter("id"));
    			
    			loadSketch = sketchDAO.getSketch(id);
    			
    			loadSketchJSON.put("id", loadSketch.getId());
				loadSketchJSON.put("sketchName", loadSketch.getSketchName());
				loadSketchJSON.put("ownerId", loadSketch.getOwnerId());
				loadSketchJSON.put("creatorId", loadSketch.getCreatorId());
				loadSketchJSON.put("createdDate", loadSketch.getCreatedDate());
				loadSketchJSON.put("modifiedDate", loadSketch.getModifiedDate());
				loadSketchJSON.put("permissions", loadSketch.getPermissions());
				loadSketchJSON.put("tags", loadSketch.getTags());
				loadSketchJSON.put("sketchData", loadSketch.getSketchData());
    			
    		} catch (JSONException e) {
    			//error
    		}
    		
    		//print to screen
    		out.println(loadSketchJSON.toString());
    	}

}
