$(document).ready(function() {
  var elems = document.querySelectorAll(".datepicker");
  var instances = M.Datepicker.init(elems);
  var carouselEl = document.getElementById("carousel-inner");
  $(instances[0].$el).change(() => $.get("/entry/", {
    date: currentLog
  })
    .done(function(data) {
      console.log(data.content);
      carouselEl.innerHTML = data.content;
    })
  );
});
