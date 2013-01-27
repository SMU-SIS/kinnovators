package com.DAO;

import com.googlecode.objectify.Query;
import com.googlecode.objectify.Objectify;
import com.googlecode.objectify.ObjectifyService;

import org.json.JSONObject;
import org.json.JSONException;
import org.json.JSONArray;

import com.model.Sketch;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;

public class SketchDAO implements java.io.Serializable {
	private static final long serialVersionUID = 1L;
	
	static {
		ObjectifyService.register(Sketch.class);
	}
	
	public SketchDAO(){
		
	}
	
	private Objectify ofy = ObjectifyService.begin();
	
	public Sketch getSketch(Long id) {
		ofy = ObjectifyService.begin();
		
		Sketch result = ofy.find(Sketch.class, id);
		return result;
	}
	
	public void addorUpdateSketch(Sketch newSketch) {
		ofy = ObjectifyService.begin();
		
		ofy.put(newSketch);
	}
	
	public void delete(Long id) {
		ofy = ObjectifyService.begin();
		
		Sketch toDelete = ofy.find(Sketch.class, id);
		ofy.delete(toDelete);
	}
	
	public List<Sketch> findSketchData() {
		ofy = ObjectifyService.begin();
		
		Query<Sketch> query = ofy.query(Sketch.class);
		List<Sketch> list = query.list();

		return list;
	}
	
	/*
	 * Under Construction
	 */
	public List<Sketch> findSketchByName(String sketchName) {
		return null;
	}
	
	public List<Sketch> findSketchByOwner(Long ownerId) {
		return null;
	}
	
	public List<Sketch> findSketchByCreator(Long creatorId) {
		return null;
	}
	
	public List<Sketch> findSketchByDateCreated(Date createdDate) {
		return null;
	}
	
	public List<Sketch> findSketchByDateModified(Date modifiedDate) {
		return null;
	}
	
	public List<Sketch> findSketchByPermissions(ArrayList<String> permissions) {
		return null;
	}
	
	public List<Sketch> findSketchByTag(String tag) {
		return null;
	}
	/*
	 * Under Construction
	 */	
}
