package com.JSON;

import com.DAO.SketchDAO;
import com.model.Sketch;

import org.json.JSONObject;
import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class ListSketch
 */
public class ListSketch extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void processRequest(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("text/html;charset=UTF-8");
		PrintWriter out = response.getWriter();
		//DAO for Sketch objects
		SketchDAO sketchDAO = new SketchDAO();
		
		ArrayList<Sketch> sketchList = (ArrayList<Sketch>) sketchDAO.findSketchData();
		
		JSONArray sketchListJSON = new JSONArray();
		try {
			for (int i = 0; i < sketchList.size(); i++) {
				Sketch sketch = sketchList.get(i);
				JSONObject sketchJSON = new JSONObject();
				
				sketchJSON.put("id", sketch.getId());
				sketchJSON.put("sketchName", sketch.getSketchName());
				sketchJSON.put("ownerId", sketch.getOwnerId());
				sketchJSON.put("creatorId", sketch.getCreatorId());
				sketchJSON.put("createdDate", sketch.getCreatedDate());
				sketchJSON.put("modifiedDate", sketch.getModifiedDate());
				sketchJSON.put("permissions", sketch.getPermissions());
				sketchJSON.put("tags", sketch.getTags());
				sketchJSON.put("sketchData", sketch.getSketchData());
				
				sketchListJSON.put(sketchJSON);
			}
		} catch (JSONException e) {
			
		}
		out.println(sketchListJSON.toString());
	}
	
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ListSketch() {
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
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		processRequest(request, response);
	}

}
