function setupDjangoPlaces(mapConfig, markerConfig, childs) {
    var latInput = childs[1];
    var lngInput = childs[2];
    var searchBox = new google.maps.places.SearchBox(childs[0]);
    var gmap = new google.maps.Map(childs[3], mapConfig);
    var marker = new google.maps.Marker(markerConfig);
    // This variable is used to track if a place from Google maps has
    // been selected after an attempt to edit the place value.
    var placeSet = false;
  
    if (latInput.value && lngInput.value) {
      var location = {
        lat: parseFloat(latInput.value),
        lng: parseFloat(lngInput.value)
      };
      marker.setPosition(location);
      marker.setMap(gmap);
      gmap.setCenter(location);
      gmap.setZoom(16);
    };

    childs[0].addEventListener("keypress", function(){
      // Set placeSet to false when place field is edited.
      placeSet = false;
    });

    childs[0].addEventListener("focusout", function (){
      // This is to prevent race between searchBox places_changed event and
      // focusout event. The searchBox places_changed event sets placeSet to
      // true.
      setTimeout(function () {
        if (!placeSet) {
          childs[0].value = "";
        }
      }, 500);
    });
  
    searchBox.addListener('places_changed', function () {
      var places = searchBox.getPlaces();
  
      if (places.length == 0) {
        return;
      }
      places.forEach(function (place) {
        if (!place.geometry) {
          console.log('Returned place contains no geometry');
          return;
        };
        if (marker) {
          marker.setMap(null);
        };
        marker.setPosition(place.geometry.location);
        marker.setMap(gmap);
        latInput.value = place.geometry.location.lat();
        lngInput.value = place.geometry.location.lng();
        gmap.setCenter(place.geometry.location);
        gmap.setZoom(16);
        // After place selection from Google maps, set placeSet to true
        placeSet = true;
        $(document).trigger('placeChanged', [{element: childs[0], place: place}]);
      });
    });
  
    google.maps.event.addListener(marker, 'dragend', function (event) {
      latInput.value = event.latLng.lat();
      lngInput.value = event.latLng.lng();
    });
  }
  
  function initDjangoPlaces() {
    var widgets = document.getElementsByClassName('places-widget');
    for (var iter = 0; iter < widgets.length; iter++) {
      setupDjangoPlaces(
        JSON.parse(widgets[iter].dataset.mapOptions),
        JSON.parse(widgets[iter].dataset.markerOptions),
        widgets[iter].children
      );
    };
  };
  
  google.maps.event.addDomListener(window, 'load', initDjangoPlaces);