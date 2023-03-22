import { WIDTHS } from "./widths.js";
import { PHOTO_METADATA } from "./photo_metadata.js";

var layout_index = -1;

function get_link_for_width(links, desired_width) {
	const widths = Object.keys(links).map(function (x) { 
  		return parseInt(x); 
	}).sort(function(a, b) {
	  return a - b;
	});
	// console.log('widths', widths);

	for (const width of widths) {
		if (width >= desired_width) {
			return links[width];
		}
	}

	const largest_width = widths[widths.length - 1];
	// console.log('returning largest image', links[largest_width]);
	return links[largest_width];
}

window.onload = () => {	
	var elements = document.getElementsByClassName("click_ends_lightbox");
	Array.from(elements).forEach(function(element) {
	  console.log('Adding event handler to click_ends_lightbox');
	  element.addEventListener('click', exitHandler);
	});

	document.addEventListener('fullscreenchange', exitHandler);
	document.addEventListener('webkitfullscreenchange', exitHandler);
	document.addEventListener('mozfullscreenchange', exitHandler);
	document.addEventListener('MSFullscreenChange', exitHandler);
}

function exitHandler() {
	console.log('exitHandler');
    if (!document.fullscreenElement && !document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
        console.log('exiting fullscreen');
        const lightbox = document.getElementById('lightbox');
        lightbox.style.display = 'none';

        const nav_bar = document.getElementById('nav_bar_anchor');
		nav_bar.style.display = 'inline';

		document.body.style.overflow = 'auto';
    }
}  

function layout() {
	// Find the largest available layout that still has a small (7%) margin.
	const border = 3;
	const margin = 20;
	const desired_width = window.innerWidth - 2 * margin - 2 * border;
	let selected_width = WIDTHS[WIDTHS.length - 1];
	for (const width of WIDTHS) {
		if (width < desired_width) {
			selected_width = width;
			break;
		}
	}

	const layouts_filename = './layouts-' + selected_width + '.js';
	import(layouts_filename).then(module => {
	    // Set the width of the Mondrian gallery div, and clear its children.
		var mondrian_gallery = document.getElementById('mondrian_gallery');
		mondrian_gallery.replaceChildren();

		// Pick a random layout of the selected width.
		if (layout_index < 0) {
			layout_index = Math.floor(Math.random() * module.LAYOUTS.length);
		}
		const layout = module.LAYOUTS[layout_index];

		const scale_factor = desired_width / selected_width;
		mondrian_gallery.style.width = window.innerWidth + 'px';
		mondrian_gallery.style.height = (scale_factor * layout['height']) + 'px';

		// Fill the Mondrian gallery with the images.
		for (const [basename, im] of Object.entries(layout['images'])) {
			const width = scale_factor * im['width'];
			const height = scale_factor * im['height'];
			const x = margin + scale_factor * im['x'];
			const y = scale_factor * im['y'];

			const link = get_link_for_width(PHOTO_METADATA[basename]['link'], width);
			const style = `position: absolute; top: ${y + border}px;` + 
				`left: ${x + border}px; width: ${width - border}px;` + 
				`height: ${height - border}px;` + im['style'];
			var img = document.createElement("img");
			img.setAttribute('src', link);
			img.setAttribute('style', style);

			img.addEventListener('click', function(){
				console.log('starting fullscreen basename', basename);

				const nav_bar = document.getElementById('nav_bar_anchor');
				nav_bar.style.display = 'none';

				document.body.style.overflow = 'hidden';

				const lightbox = document.getElementById('lightbox');
				lightbox.replaceChildren();

				const link = get_link_for_width(PHOTO_METADATA[basename]['link'], 10000);
				console.log('lightbox link', link);
				var img = document.createElement("img");
				img.setAttribute('src', link);

				img.addEventListener('click', function() {
					console.log('lightbox img click handler');
					document.exitFullscreen();
				});

				lightbox.appendChild(img);
				lightbox.style.display = 'block';

				lightbox.requestFullscreen();
			});

			mondrian_gallery.appendChild(img);
		}
    });
}

// Run the layout function at load, and also whenever the user resizes the
// window.
layout();
window.onresize = layout;