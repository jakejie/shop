(function() {

 "use strict";
 
	// Hone page one Revolution Slider Initialize			
	jQuery('.fullwidthbanner').show().revolution(
	{
		dottedOverlay:"none",
		delay:9000,
		startwidth:1920,
		startheight:800,
		hideThumbs:200,

		thumbWidth:100,
		thumbHeight:50,
		thumbAmount:2,
		
		simplifyAll:"off",
		
		navigationType:"bullet",
		navigationArrows:"solo",
		navigationStyle:"preview1",
		
		touchenabled:"on",
		onHoverStop:"on",
		nextSlideOnWindowFocus:"off",
		
		swipe_threshold: 75,
		swipe_velocity: 0.7,
		swipe_min_touches: 1,
		swipe_max_touches: 1,
		drag_block_vertical: false,
								
		keyboardNavigation:"off",
		
		navigationHAlign:"center",
		navigationVAlign:"bottom",
		navigationHOffset:0,
		navigationVOffset:20,

		soloArrowLeftHalign:"left",
		soloArrowLeftValign:"center",
		soloArrowLeftHOffset:20,
		soloArrowLeftVOffset:0,

		soloArrowRightHalign:"right",
		soloArrowRightValign:"center",
		soloArrowRightHOffset:20,
		soloArrowRightVOffset:0,
				
		shadow:0,
		fullWidth:"on",
		fullScreen:"off",

		spinner:"spinner0",
		
		stopLoop:"off",
		stopAfterLoops:-1,
		stopAtSlide:-1,
		
		hideTimerBar:"on",

		shuffle:"off",
		
		autoHeight:"off",						
		forceFullWidth:"off",
								
		hideThumbsOnMobile:"off",
		hideNavDelayOnMobile:1500,						
		hideBulletsOnMobile:"off",
		hideArrowsOnMobile:"off",
		hideThumbsUnderResolution:0,
		
		hideSliderAtLimit:0,
		hideCaptionAtLimit:0,
		hideAllCaptionAtLilmit:0,
		startWithSlide:0,
		videoJsPath:"rs-plugin/videojs/",
		fullScreenOffsetContainer: ""	
	});
	
 
	
})();	