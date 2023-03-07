// $(document).ready(function()
// {
// 	// When the user clicks on any overlay element, stop the lightbox mode.
// 	$(".click_ends_lightbox").click(function() { stopLightbox(); });
	
// 	// Disable scrolling the background when the lightbox is open.
// 	// See http://stackoverflow.com/questions/8332258/how-do-i-undo-preventdefault-on-touchmove
// 	document.body.addEventListener("touchmove", function(e) {
// 	  if($("#curtain").is(":visible")){
// 		   e.preventDefault(); 
// 	  }   
// 	}, false);
// });

// function startLightbox(image)
// {
// 	// Clear the slide
// 	$("#slide_0 img").attr('src', '/static/image/transparent.png');
	
// 	// Show the curtain and the loading spinner
// 	$("#curtain").show();
// 	$("#loading_spinner").show();
	
// 	// Set the image's url (which begins downloading it). When done
// 	// loading, fade the slide in.
// 	$("#slide_0 img").attr('src', image.url_l);
// 	$("#slide_0 img").load(function() {
//   		$("#slide_0").fadeIn();
//   		$("#loading_spinner").fadeOut();
// 	});
		
// 	// Prevent the background from scrolling while the lightbox is open
// 	// See http://stackoverflow.com/questions/3656592/programmatically-disable-scrolling
// 	$("body").css("overflow", "hidden");
	
// 	// Set the URL's hash tag (anchor portion) for deep-linking to this photo
// 	window.location.hash = image.title;
	
// 	// Fetch a URL from the server; this indicates a "vote" for the photo
// 	$.getJSON("/vote/" + image.title, function(response) {});
// }

// function stopLightbox()
// {
// 	// To stop the lightbox, simply hide all overlays.
// 	$(".overlay").hide();
	
// 	// Re-enable scrolling
// 	$("body").css("overflow", "visible");
	
// 	// Clear the hash tag part of the URL
// 	window.location.hash = '';
// }
