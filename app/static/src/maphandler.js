var mymap = L.map("mapid").setView([-36.2409, -60.13916], 6);
L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWd1c3RpbnJvdyIsImEiOiJja2d4MXZsM24wZnRqMnpuMDVneGg0cXU2In0.dW1nslyNz7KEQuh38PTqug",
  {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: "your.mapbox.access.token",
  }
).addTo(mymap);

var marker;
function onMapClick(e) {
  if (marker) {
    mymap.removeLayer(marker);
  }
  console.log(e);
  marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(mymap);
  mymap.setView([e.latlng.lat, e.latlng.lng], (zoom = 16));
  document.forms[0].latitudCentro.value = e.latlng.lat;
  document.forms[0].longitudCentro.value = e.latlng.lng;
}
mymap.on("click", onMapClick);

if ($("#latitudCentro").val() != 0 && $("#longitudCentro").val() != 0) {
  latLng = L.latLng($("#latitudCentro").val(), $("#longitudCentro").val());
  marker = L.marker(latLng).addTo(mymap);
  mymap.setView(latLng, (zoom = 10));
}
