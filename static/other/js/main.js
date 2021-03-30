;(function($, window, document, undefined) {
    "use strict";

    /*============================*/
	/* 01 - VARIABLES */
	/*============================*/
	
	var swipers = [], winW, winH, winScr, _isresponsive, smPoint = 768, mdPoint = 992, lgPoint = 1200, addPoint = 1600, _ismobile = navigator.userAgent.match(/Android/i) || navigator.userAgent.match(/webOS/i) || navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPad/i) || navigator.userAgent.match(/iPod/i);


	/*========================*/
	/* 02 - PAGE CALCULATIONS */
	/*========================*/
	function pageCalculations(){
		winW = $(window).width();
		winH = $(window).height();
	}
    

	/*=================================*/
	/* 03 - FUNCTION ON DOCUMENT READY */
	/*=================================*/
	pageCalculations();
	

	/*============================*/
	/* 04 - FUNCTION ON PAGE LOAD */
	/*============================*/
	
	$(window).on("load", function(){	
		heightPage();	
	    setTimeout(function(){
	    	initSwiper();
	    },0);
    
    	$(".wpc-preloader").fadeOut();
	});


	/*==============================*/
	/* 05 - FUNCTION ON PAGE RESIZE */
	/*==============================*/	

	function resizeCall(){
		pageCalculations();
		$('.swiper-container.initialized[data-slides-per-view="responsive"]').each(function(){
			var thisSwiper = swipers['swiper-'+$(this).attr('id')], $t = $(this), slidesPerViewVar = updateSlidesPerView($t), centerVar = thisSwiper.params.centeredSlides;
			thisSwiper.params.slidesPerView = slidesPerViewVar;
			thisSwiper.reInit();
			if(!centerVar){
				var paginationSpan = $t.find('.pagination span');
				var paginationSlice = paginationSpan.hide().slice(0,(paginationSpan.length+1-slidesPerViewVar));
				if(paginationSlice.length<=1 || slidesPerViewVar>=$t.find('.swiper-slide').length) $t.addClass('pagination-hidden');
				else $t.removeClass('pagination-hidden');
				paginationSlice.show();
			}
		});	
	}
	if(!_ismobile){
		$(window).resize(function(){
			resizeCall();
		});
	} else{
		window.addEventListener("orientationchange", function() {
			resizeCall();
		}, false);
	}

	/***********************************/
	/* RUN RESIZE FUNCTIONS */
	/**********************************/
    
	$(window).on('resize', function () {
        heightSidebar(); 
        heightPage();
        arrowSlider();
        removeNoScroll();
        clickMenu();
        // toggleMenu();
	 });
	

	/***********************************/
	/* RUN SCROLL FUNCTIONS */
	/**********************************/

    $(window).on('scroll', function () {
        wpcProgress();
        timer(); 
	 });

    /******************************************/
	/* DYNAMIC CHANGE CONTENT IN HOME SIDEBAR */
	/*****************************************/

	function homeSidebar() {
		$(".home-s-tile").text($(".wpc-main-slider .swiper-slide-active .slide-wrap").attr("data-title"));
		$(".home-s-desc").text($(".wpc-main-slider .swiper-slide-active .slide-wrap").attr("data-desc"));
	}
	

	/*=====================*/
	/* 07 - SWIPER SLIDERS */
	/*=====================*/
    
	function initSwiper(){
		var initIterator = 0;
		$('.swiper-container').each(function(){								  
			var $t = $(this);								  

			var index = 'swiper-unique-id-'+initIterator;

			$t.addClass('swiper-'+index + ' initialized').attr('id', index);
			$t.find('.pagination').addClass('pagination-'+index);

			var autoPlayVar = parseInt($t.attr('data-autoplay'),10);
            var mode = $t.attr('data-mode');
			var slidesPerViewVar = $t.attr('data-slides-per-view');
			if(slidesPerViewVar == 'responsive'){
				slidesPerViewVar = updateSlidesPerView($t);
			}
			else slidesPerViewVar = parseInt(slidesPerViewVar,10);

			var loopVar = parseInt($t.attr('data-loop'),10);
			var speedVar = parseInt($t.attr('data-speed'),10);
            var centerVar = parseInt($t.attr('data-center'),10);
			swipers['swiper-'+index] = new Swiper('.swiper-'+index,{
				speed: speedVar,
				pagination: '.pagination-'+index,
				loop: loopVar,
				paginationClickable: true,
				autoplay: autoPlayVar,
				slidesPerView: slidesPerViewVar,
				keyboardControl: true,
				calculateHeight: true, 
				simulateTouch: true,
				roundLengths: true,
				centeredSlides: centerVar,
                mode: mode || 'horizontal',
				onInit: function(swiper){
				    $t.find('.swiper-slide').addClass('active');
				    homeSidebar();
				},
				onSlideChangeEnd: function(swiper){
					var activeIndex = (loopVar===1)?swiper.activeLoopIndex:swiper.activeIndex;
					var qVal = $t.find('.swiper-slide-active').attr('data-val');
					$t.find('.swiper-slide[data-val="'+qVal+'"]').addClass('active');
				},
				onSlideChangeStart: function(swiper){
					$t.find('.swiper-slide.active').removeClass('active');
					homeSidebar();
                    
				}
			});
			swipers['swiper-'+index].reInit();
				if($t.attr('data-slides-per-view')=='responsive'){
					var paginationSpan = $t.find('.pagination span');
					var paginationSlice = paginationSpan.hide().slice(0,(paginationSpan.length+1-slidesPerViewVar));
					if(paginationSlice.length<=1 || slidesPerViewVar>=$t.find('.swiper-slide').length) $t.addClass('pagination-hidden');
					else $t.removeClass('pagination-hidden');
					paginationSlice.show();
				}
            
            if($t.find('.default-active').length){
                swipers['swiper-'+index].swipeTo($t.find('.swiper-slide').index($t.find('.default-active')), 0);    
            } 
            
			initIterator++; 
		});
		
	}

	function updateSlidesPerView(swiperContainer){
		if(winW>=addPoint) return parseInt(swiperContainer.attr('data-add-slides'),10);
		else if(winW>=lgPoint) return parseInt(swiperContainer.attr('data-lg-slides'),10);
		else if(winW>=mdPoint) return parseInt(swiperContainer.attr('data-md-slides'),10);
		else if(winW>=smPoint) return parseInt(swiperContainer.attr('data-sm-slides'),10);
		else return parseInt(swiperContainer.attr('data-xs-slides'),10);
	}	


	//swiper arrows
	$('.swiper-arrow-left').on('click', function(){
		swipers['swiper-'+$(this).parent().attr('id')].swipePrev();
	});

	$('.swiper-arrow-right').on('click', function(){
		swipers['swiper-'+$(this).parent().attr('id')].swipeNext();
	});
    
    $('.swiper-outer-left').on('click', function(){
		swipers['swiper-'+$('.home-slider').attr('id')].swipePrev();
	});

	$('.swiper-outer-right').on('click', function(){
		swipers['swiper-'+$('.home-slider').attr('id')].swipeNext();
	});

	$('.swiper-arr-left').on('click', function(){
		swipers['swiper-'+$('.wpc-gallery-slider').attr('id')].swipePrev();
	});

	$('.swiper-arr-right').on('click', function(){
		swipers['swiper-'+$('.wpc-gallery-slider').attr('id')].swipeNext();
	});
    
	


	$(".menu-toggle.toggle-classic").on("click", function(){
		$("html").toggleClass("no-y-scroll");
	});

	function toggleMenu() {
		$(".menu-toggle").on("click", function(){
			if($(window).width()<768) {
				$("html").toggleClass("no-scroll-y");
			}			
		});
	}
	toggleMenu();

	function removeNoScroll() {
		if($(window).width()>767) {
			$("html").removeClass("no-scroll-y");
		} 
		if($(".wpc-menu").hasClass("open-menu") && $(window).width()<768) {
			$("html").addClass("no-scroll-y");
		}
	}
	removeNoScroll();
	
   function arrowSlider() {
   		$(".btn-toggle-slider.classic").css("top", $(window).height()/2);
   }

   arrowSlider();

	
    
    
    
    /***********************************/
	/*BACKGROUND*/
	/**********************************/
    
    //sets child image as a background
    $('.s-back-switch').each(function(){
        var $img = $(this).find('.s-img-switch');
        var $imgSrc =  $img.attr('src');
        var $imgDataHidden =  $img.data('s-hidden');
        $(this).css('background-image' , 'url(' + $imgSrc + ')');
        if($imgDataHidden){
        	$img.css('visibility', 'hidden');
        }else{
        	$img.hide();
        }
    });

    /***********************************/
	/*SIDEBAR AND MENU EVENT*/
	/**********************************/

    $(".wpc-menu .menu-toggle").on("click", function(){
    	$(this).parent().toggleClass("open-menu");
    	if($(this).parent().hasClass("open-menu")) {
    		setTimeout(function(){
    			$(".wpc-menu.open-menu .nav-wrap").css("overflow", "visible");
    		}, 500)
    	} else {
    		$(".wpc-menu .nav-wrap").css("overflow", "hidden");
    	}
    	if($(window).width()>1199) {
    		if($(this).parent().hasClass("open-menu")) {
	    		$(".wpc-logo .pages").fadeOut(100);
	    	} else {   			
	    			setTimeout(function(){
			    		$(".wpc-logo .pages").fadeIn(100);
			    	}, 500);
	    	}
    	}	
    	
    });

    function clickMenu() {
	    if($(window).width()<768) {
	    	$(".wpc-menu .main-menu > .menu-item-has-children a, .wpc-menu .main-menu > .menu-item.menu-item-has-children .submenu .menu-item a").on("click", function(){           
                if($(this).attr('href')!='#') {
                    $(this).next().slideToggle();
                    return false;
                } 
            });
	    } 
	    if($(window).width()<992 && $(window).width()>768) {
	    	$(".wpc-menu.classic .menu-item.menu-item-has-children a").on("click", function(){           
                if($(this).attr('href')!='#') {
                    $(this).next().slideToggle();
                    return false;
                } 
            });
	    }
    }
    clickMenu();


    $(".wpc-menu .sidebar-toggle").on("click", function(){
    	$(".wpc-sidebar").addClass("active");
    });

    $(".wpc-sidebar .fa-times").on("click", function(){
    	$(".wpc-sidebar").removeClass("active");
    });


    /***********************************/
	/*POPUP*/
	/**********************************/

	if($(".popup-gallery").length) {
		$('.popup-gallery').magnificPopup({
			delegate: '.magnific-popup-link',
			type: 'image',
			tLoading: 'Loading image #%curr%...',
			mainClass: 'mfp-with-zoom',
			gallery: {
				enabled: true,
				navigateByImgClick: true
			},
			callbacks: {                    
                markupParse: function (template, values, item) {
                    values.title = item.el.attr('title'); 
                }
            },
			zoom: {
			    enabled: true, // By default it's false, so don't forget to enable it

			    duration: 300, // duration of the effect, in milliseconds
			    easing: 'ease-in-out' // CSS transition easing functio
			  }
		});
	}





 	/***********************************/
	/* COUNTERS */
	/**********************************/
   
    
	function timer() {
		$('.wpc-timer').not('.animated').each(function(){
			if($(window).scrollTop() >= $(this).offset().top-$(window).height()*1.1 )  {
				$(this).addClass('animated').countTo();
			}
		});
	}
    
    timer();

    
    /***********************************/
	/* SKILLS */
	/**********************************/



    function wpcProgress(){
	    if($('.wpc-skills').length) {
	         $('.wpc-skills').not('.animated').each(function(){
	            var self = $(this);    
	            if($(window).scrollTop() >= self.offset().top - $(window).height() ){
	                self.addClass('animated').find('.timer').countTo();

	                self.find('.line-fill').each(function(){
	                    var objel = $(this);
	                    var pb_width = objel.attr('data-width-pb');
	                    objel.css({'width':pb_width});
	                });
	            }

	         });      
	     }
	}    

	wpcProgress();

	 

	/***********************************/
	/* HEIGHT SIDEBAR */
	/**********************************/
	

	function heightSidebar(){
		var cols = $('.wpc-sidebar.sidebar-h'); 
		if($(window).width()>991) {			         
            cols.css('height', '100%');
            setTimeout(function(){
                cols.outerHeight($(document).height());    
            },2000);  

		} else{
			cols.css('height', '100%');
		}
    }

	heightSidebar();


	function heightPage() {		
		if($(".wpc-h").length && $(".wpc-h").hasClass("gallery")) {
			if($(window).width()>1199) {
				$(".wpc-h").css("height", ($(window).height()-($(".wpc-header").outerHeight(true)+$(".wpc-footer").outerHeight(true)))/3);
				$("html").addClass("no-scroll");
			} else {
				$(".wpc-h").css({"height": "auto", "min-height": "293px"});
				$("html").removeClass("no-scroll");
			}			
		}	
		 else {
			$(".wpc-h").css("height", $(window).height()-($(".wpc-header").outerHeight(true)+$(".wpc-footer").outerHeight(true))-15 );
			if($(window).width()>1199) {
				if($(".wpc-h").length && $(".wpc-h").hasClass("full-page")) {
					$("html").addClass("no-scroll");
				}
			} else {
				$(".wpc-h").css({"height": "auto"});
				$("html").removeClass("no-scroll");
			}
				
		}
		
	}


	/***********************************/
	/* MASONRY */
	/**********************************/


	$('.grid').masonry({
	  // options...
	  itemSelector: '.grid-item'
	  // columnWidth: 200
	});



	/***********************************/
	/* GOOGLE MAPS */
	/**********************************/


	if( $('.wpc-map').length ) {
		$('.wpc-map').each(function() {
			initialize(this);
		});
	}

	function initialize(_this) {
		
		var stylesArray = {
			//style 1
			'style-1' : [{"featureType":"administrative.country","elementType":"labels.text","stylers":[{"visibility":"on"}]}]
		};

		var styles ,map, marker, infowindow,
			lat = $(_this).attr("data-lat"),
	   		lng = $(_this).attr("data-lng"),
			contentString = $(_this).attr("data-string"),
			image = $(_this).attr("data-marker"),
			styles_attr = $(_this).attr("data-style"),
			zoomLevel = parseInt($(_this).attr("data-zoom"),10),
			myLatlng = new google.maps.LatLng(lat,lng);
			

		// style_1
		if (styles_attr == 'style-1') {
			styles = stylesArray[styles_attr];
		}
		// custom
		if (typeof hawa_style_map != 'undefined' && styles_attr == 'custom') {
			styles = hawa_style_map;
		}
		// or default style
		
		var styledMap = new google.maps.StyledMapType(styles,{name: "Styled Map"});
	    
		var mapOptions = {
			zoom: zoomLevel,
			disableDefaultUI: true,
			center: myLatlng,
	        scrollwheel: false,
			mapTypeControlOptions: {
	        mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
			},
			draggableCursor: 'url(img/mapHover.png) 64 64, move'
		};

		
		map = new google.maps.Map(_this, mapOptions);

		map.mapTypes.set('map_style', styledMap);
		map.setMapTypeId('map_style');

		infowindow = new google.maps.InfoWindow({
			content: contentString
		});
	  
	    
	    marker = new google.maps.Marker({
			position: myLatlng,
			map: map,
			icon: image
		});

		google.maps.event.addListener(marker, 'click', function() {
			infowindow.open(map,marker);
		});

	}

    

    


   
      
})(jQuery, window, document);
