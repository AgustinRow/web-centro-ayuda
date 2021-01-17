$("#datepair .time").timepicker({
  minTime: "9:00",
  maxTime: "16:00",
  timeFormat: "H:i",
});

var timeOnlyExampleEl = document.getElementById("datepair");
var timeOnlyDatepair = new Datepair(timeOnlyExampleEl);
