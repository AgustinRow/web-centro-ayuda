function getMunicipios() {
  $.ajax({
    type: "GET",
    url: "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios",
    dataType: "json",
    success: function (data, msg) {
      var text = "";
      municipio = $("#municipioCentro").val();
      $.each(data.data.Town, function (key, val) {
        if (val.name == municipio) {
          text +=
            "<option selected values=" +
            val.name +
            ">" +
            val.name +
            "</option>";
        } else {
          text += "<option values=" + val.name + ">" + val.name + "</option>";
        }
      });
      var countries = document.getElementById("municipioCentro");
      countries.insertAdjacentHTML("beforeEnd", text);
    },
    error: function (msg) {
      console.table(msg);
    },
  });
}
getMunicipios();
