$(document).ready(function() {
  var elems = document.querySelectorAll(".datepicker");
  var instance = M.Datepicker.init(elems, {"autoClose": true, "defaultDate": new Date(), "setDefaultDate": true})[0];
  var carouselEl = document.getElementById("carousel-inner");
  $(instance.$el).change(() => $.get("/entry/", {
    date: instance.date.toISOString().substring(0, 10)
  })
    .done(function(data) {
      carouselEl.innerHTML = data.content;
    })
    .fail(function(data) {
      carouselEl.innerHTML = "No entry.";
    })
  );
  $("#prev-button").click(() => {
    instance.setDate(new Date(instance.date - 1));
    instance._finishSelection();
  });
  $("#next-button").click(() =>{
    instance.setDate(new Date(Number(instance.date) + 24*60*60000))
    instance._finishSelection();
  });
  $(instance.$el).change();
});