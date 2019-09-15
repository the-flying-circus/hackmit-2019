$(document).ready(function() {
  var elems = document.querySelectorAll(".datepicker");
  var instance = M.Datepicker.init(elems, {"autoClose": true, "defaultDate": new Date(), "setDefaultDate": true})[0];
  var carouselEl = document.getElementById("carousel-inner");
  $(instance.$el).change(() => $.get(`/pages/${instance.date.toISOString().substring(0, 10)}/?format=json`)
    .done(function(data) {
      carouselEl.innerHTML = data.content;
      console.log(data);
      let emoticon_dict = {};
      for (let i = 0; i < data.metric_set.length; i++)
        emoticon_dict[data.metric_set[i]["name"]] = data.metric_set[i]["value"];
      document.getElementById("mood-emoticon").innerHTML = `<img src="/static/images/emots/${emoticon_dict['mood']}.png">`;
      document.getElementById("anxiety-emoticon").innerHTML = `<img src="/static/images/emots/${emoticon_dict['anxiety']}.png">`;
      document.getElementById("cynicism-emoticon").innerHTML = `<img src="/static/images/emots/${emoticon_dict['cynicism']}.png">`;
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
  addPageLoadEvent(5, () => $(instance.$el).change());
});
