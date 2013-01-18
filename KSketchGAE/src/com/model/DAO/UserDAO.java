/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.model.DAO;

import com.model.entity.User;
import java.util.*;
import java.text.SimpleDateFormat;


import com.googlecode.objectify.Objectify;
import com.googlecode.objectify.ObjectifyService;
import com.googlecode.objectify.Query;


/**
 *
 * @author kwgoh.2010
 */
@SuppressWarnings({ "serial", "unused" })
public class UserDAO implements java.io.Serializable {
    static {
		ObjectifyService.register(User.class);
	}
	
	//public static final String DB_LOOKUP = "java:comp/env/jdbc/ksketchtestdb";

	private Objectify ofy = ObjectifyService.begin();
    
	public UserDAO() {

	}
	
    public User create(String username, String password, String email) {
		User user = null;
		
    	ArrayList<User> list = (ArrayList<User>) retrieveAll();
    	
    	for (int i = 0; i < list.size(); i++) {
    		if (list.get(i).getUsername().equals(username)) {
    			user = list.get(i);
    			break;
    		}
    	}
		
		if (user == null) {
	    	if (!username.equals("") || !password.equals("") || !email.equals("")) {
				user = new User(username, password, email);
				ofy.put(user);
			}
			return user;
		}
		else {
			return null;
		}
    }

    /*public User createFacebook(String facebookEmail) {
        User user = new User(facebookEmail);

        //sql code goes here
        return user;
    }*/

    /*public User createGooglePlus(String googlePlusEmail) {
        User user = new User(googlePlusEmail);

        //sql code goes here
        return user;
    }*/

    public List<User> retrieveAll() {
    	Query<User> q = ofy.query( User.class);

    	return q.list();    
    }
    
    public User retrieve(String username) {
    	User user = null;
    	
    	ArrayList<User> list = (ArrayList<User>) retrieveAll();
    	
    	for (int i = 0; i < list.size(); i++) {
    		if (list.get(i).getUsername().equals(username)) {
    			user = list.get(i);
    			break;
    		}
    	}
        return user;
    }

    public User retrieveLogin(String username, String password) {
    	User user = null;
    	
    	ArrayList<User> list = (ArrayList<User>) retrieveAll();
    	
    	for (int i = 0; i < list.size(); i++) {
    		if (list.get(i).getUsername().equals(username)) {
    			if (list.get(i).getPassword().equals(password)) {
	    			user = list.get(i);
	    			break;
    			}
    		}
    	}
        return user;
    }

    /*public User retrieveFacebook(String facebookEmail) {

        //code to retrieve user;
        return null;
    }*/

    /*public User retrieveGooglePlus(String googlePlusEmail) {

        //code to retrieve user;
        return null;
    }*/

    public User update(String username, String password, String email, String firstname, String lastname, String description) {
    	
		User user = null;
    	ArrayList<User> list = (ArrayList<User>) retrieveAll();
    	
    	for (int i = 0; i < list.size(); i++) {
    		if (list.get(i).getUsername().equals(username)) {
    			user = list.get(i);
    			user.setPassword(password);
    			user.setEmail(email);
    			user.setFirstname(firstname);
    			user.setLastname(lastname);
    			user.setDescription(description);
    			break;
    		}
    	}
		if (user != null) {
			ofy.put(user);
		}
        return user;
    }

    public int toggleActivation(String username) {
    	
		User user = null;
		int status = -1;

    	ArrayList<User> list = (ArrayList<User>) retrieveAll();
    	
    	for (int i = 0; i < list.size(); i++) {
    		if (list.get(i).getUsername().equals(username)) {
    			user = list.get(i);
    			if (user.isActive()) {
    				user.setActive(false);
    				status=0;
    			} else {
    				user.setActive(true);
    				status=1;
    			}
    			break;
    		}
    	}
		if (user != null) {
			ofy.put(user);
		}
        return status;
    }    
    
    /*public User updateFacebook(String facebookEmail) {

        //code to retrieve user;
        //code to update user;
        return null;
    }*/

    /*public User updateGooglePlus(String googlePlusEmail) {

        //code to retrieve user;
        //code to update user;
        return null;
    }*/

    public User delete(String username) {

        //code to retrieve user;
        //code to delete user;
        return null;
    }
}
