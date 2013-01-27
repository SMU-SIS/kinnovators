package com.model;

import javax.persistence.Id;

import java.util.ArrayList;
import java.util.Date;

public class Sketch {
	
	@Id
	Long id;
	private String sketchName;
	private Long ownerId;
	private Long creatorId;
	private Date createdDate;
	private Date modifiedDate;
	private ArrayList<String> permissions;
	private ArrayList<String> tags;
	private String sketchData;

	//Blank Constructor needed to make GAE Persistance/Objectify work.
	public Sketch() {
		
	}
	
	//Constructor - Save New Sketch
	public Sketch (String sketchName, Long ownerId, Date createdDate, ArrayList<String> permissions, String sketchData) {
		
		this.sketchName = sketchName;
		this.ownerId = ownerId;
		creatorId = ownerId;
		this.createdDate = createdDate;
		modifiedDate = createdDate;
		this.permissions = permissions;
		tags = new ArrayList<String>();
		this.sketchData = sketchData;
	}
	
	//Constructor - Copy Sketch
	public Sketch (String sketchName, Long ownerId, Long creatorId, Date createdDate, Date modifiedDate, ArrayList<String> permissions, ArrayList<String> tags, String sketchData) {
		
		this.sketchName = sketchName;
		this.ownerId = ownerId;
		this.creatorId = creatorId;
		this.createdDate = createdDate;
		this.modifiedDate = modifiedDate;
		this.permissions = permissions;
		this.tags = tags;
		this.sketchData = sketchData;
	}

	//Constructor - Update Existing Sketch
	public Sketch (Long id, String sketchName, Long ownerId, Long creatorId, Date createdDate, Date modifiedDate, ArrayList<String> permissions, ArrayList<String> tags, String sketchData) {
		
		this.id = id;
		this.sketchName = sketchName;
		this.ownerId = ownerId;
		this.creatorId = creatorId;
		this.createdDate = createdDate;
		this.modifiedDate = modifiedDate;
		this.permissions = permissions;
		this.tags = tags;
		this.sketchData = sketchData;
	}
	
	public String getSketchName() {
		return sketchName;
	}

	public ArrayList<String> getTags() {
		return tags;
	}

	public void setTags(ArrayList<String> tags) {
		this.tags = tags;
	}

	public void setSketchName(String sketchName) {
		this.sketchName = sketchName;
	}

	public Long getOwnerId() {
		return ownerId;
	}

	public void setOwnerId(Long ownerId) {
		this.ownerId = ownerId;
	}

	public Long getCreatorId() {
		return creatorId;
	}

	public void setCreatorId(Long creatorId) {
		this.creatorId = creatorId;
	}

	public Date getCreatedDate() {
		return createdDate;
	}

	public void setCreatedDate(Date createdDate) {
		this.createdDate = createdDate;
	}

	public Date getModifiedDate() {
		return modifiedDate;
	}

	public void setModifiedDate(Date modifiedDate) {
		this.modifiedDate = modifiedDate;
	}

	public ArrayList<String> getPermissions() {
		return permissions;
	}

	public void setPermissions(ArrayList<String> permissions) {
		this.permissions = permissions;
	}

	public String getSketchData() {
		return sketchData;
	}

	public void setSketchData(String sketchData) {
		this.sketchData = sketchData;
	}

	public Long getId() {
		return id;
	}
	
	
}
