// JavaScript Document
function saveKSketchFile(fileData)
{
	alert(fileData);	
	var file = textToXML(fileData);
	saveCtrl(file);
	loadKSketchFile(file);
}

//Convert a string to XML Node Structure
//Returns null on failure
function textToXML (fileData) {
   try {
     var xml = null;

     if ( window.DOMParser ) {

       var parser = new DOMParser();
       xml = parser.parseFromString(fileData, "text/xml" );

       var found = xml.getElementsByTagName( "parsererror" );

       if ( !found || !found.length || !found[ 0 ].childNodes.length ) {
    	   return xml;
       }

       return null;
     } else {

       xml = new ActiveXObject( "Microsoft.XMLDOM" );

       xml.async = false;
       xml.loadXML(fileData);

       return xml;
     }
   } catch ( e ) {
     // suppress
   }
 }

function saveCtrl(file) {
	alert(file);
	
    var fd = new FormData();

    fd.append( "file", file);
    $.ajax({
        url: 'BlobServlet',
        type: 'POST',
        cache: false,
        data: fd,
        processData: false,
        contentType: false,
    });
}

function loadKSketchFile(fileData)
{
	var swfObject = document.getElementById('KSketch2_Web');
	if(typeof swfObject !='undefined'){
		alert("loading file!")
		swfObject.loadKSketchFile(fileData);
	}
	else
	{
		alert('the swf object does not exist!');
	}	
}