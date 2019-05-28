$(function() {
  // use below if you want to specify the path for leaflet's images
  //L.Icon.Default.imagePath = '@Url.Content("~/Content/img/leaflet")';

  var curLocation = [0, 0];
  // use below if you have a model
  // var curLocation = [@Model.Location.Latitude, @Model.Location.Longitude];

  if (curLocation[0] == 0 && curLocation[1] == 0) {
    curLocation = [5.9714, 116.0953];
  }

  var map = L.map('MapLocation').setView(curLocation, 10);

  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  map.attributionControl.setPrefix(false);

  var marker = new L.marker(curLocation, {
    draggable: 'true'
  });

  marker.on('dragend', function(event) {
    var position = marker.getLatLng();
    marker.setLatLng(position, {
      draggable: 'true'
    }).bindPopup(position).update();
    $("#Latitude").val(position.lat);
    $("#Longitude").val(position.lng).keyup();
  });

  $("#Latitude, #Longitude").change(function() {
    var position = [parseInt($("#Latitude").val()), parseInt($("#Longitude").val())];
    marker.setLatLng(position, {
      draggable: 'true'
    }).bindPopup(position).update();
    map.panTo(position);
  });

  map.addLayer(marker);
})