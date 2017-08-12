var webhook = 'https://hooks.zapier.com/hooks/catch/1443994/4be9du/';

function arrayToObj(arr) {
  var obj = {}
  for (var i=0; i < arr.length; i++) {
    obj[arr[i].name] = arr[i].value;
  }
  return obj;
}

var $form = $('form');

$('form .wsite-button').click(function() {
  var data = arrayToObj($('form').serializeArray());
  $.post(webhook, data, function(res) {
    $form.hide();
    $form.parent().append('<span class="success-msg">Awesome! Will get back to you soon</span>');
  })
  .fail(function() {
    $form.prepend('<span class="fail-msg">Oops, something went wrong.</span>');
  });
});
