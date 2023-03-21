$(document).ready(function() {
    // when user clicks add more btn of images
  $('.add-images').click(function(ev) {
      ev.preventDefault();
      var count = $('#item-images').children().length;
      var tmplMarkup = $('#images-template').html();
      var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
      $('#item-images').append(compiledTmpl);

      // update form count
      $('#id_images-TOTAL_FORMS').attr('value', count+1);
  });
});