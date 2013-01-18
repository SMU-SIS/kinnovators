/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.model.entity;

import javax.persistence.Id;
import javax.persistence.Transient;
import java.util.*;

/**
 *
 * @author kwgoh.2010
 */
public class User implements java.io.Serializable {  
	
	@Id private Long id;
    private String username;
    private String password;
    private String email;
    private Date registeredDate;
    private String facebookEmail;
    private String googlePlusEmail;
    private double appVersion;
    private String firstname;
    private String lastname;
    private String description;
    private boolean active;

public User(){}
    

    
    public User (String username, String password, String email) {
        
        this.username = username;
        this.password = password;
        this.email = email;
        this.active = true;
        registeredDate = new Date();
    }
    
    // facebook/google plus login
    public User (String email) {
        
        if (email.indexOf("@facebook.com") != -1) {
        this.facebookEmail = email;
        }
        if (email.indexOf("@gmail.com") != -1) {
            this.googlePlusEmail = email;
        }
        registeredDate = new Date();
    }
    
    /*public User (String googlePlusEmail) {
        
        this.googlePlusEmail = googlePlusEmail;
        registeredDate = new Date();
    }*/
    

    public User(String username, String password, String email,
			String facebookEmail, String googlePlusEmail,
			double appVersion, String firstname, String lastname,
			String description, boolean active, Date registeredDate) {
		super();
		this.username = username;
		this.password = password;
		this.email = email;
		this.registeredDate = registeredDate;
		this.facebookEmail = facebookEmail;
		this.googlePlusEmail = googlePlusEmail;
		this.appVersion = appVersion;
		this.firstname = firstname;
		this.lastname = lastname;
		this.description = description;
		this.active = active;
	}

	public String getFirstname() {
		return firstname;
	}

	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}

	public String getLastname() {
		return lastname;
	}

	public void setLastname(String lastname) {
		this.lastname = lastname;
	}

	public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public double getAppVersion() {
        return appVersion;
    }

    public void setAppVersion(double appVersion) {
        this.appVersion = appVersion;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFacebookEmail() {
        return facebookEmail;
    }

    public void setFacebookEmail(String facebookEmail) {
        this.facebookEmail = facebookEmail;
    }

    public String getGooglePlusEmail() {
        return googlePlusEmail;
    }

    public void setGooglePlusEmail(String googlePlusEmail) {
        this.googlePlusEmail = googlePlusEmail;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Date getRegisteredDate() {
        return registeredDate;
    }

    public void setRegisteredDate(Date registeredDate) {
        this.registeredDate = registeredDate;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }  
    
    public Long getID(){
    	return id;
    }
    
}
