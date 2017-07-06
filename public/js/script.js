$(document).ready(function(){
    $("#text-input").focus();
});

$("#submit-input").on('click', function(){
    var xhr = new XMLHttpRequest();
    var params = {
        data: $("#text-input").val()
    };
	xhr.onreadystatechange = function () {
		if(this.readyState == 4 && this.status == 200){
			updateOutput(this.responseText);
		}
	};
	xhr.open("POST", "/parse", true);
	xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify(params));
});

function updateOutput(data) {
    $("#text-output").focus();
    document.getElementById("text-output").value = JSON.stringify(JSON.parse(data), undefined, 4);
    $('#text-output').trigger('autoresize');
};


$(document).delegate('#text-input', 'keydown', function(e) {
  var keyCode = e.keyCode || e.which;

  if (keyCode == 9) {
    e.preventDefault();
    var start = $(this).get(0).selectionStart;
    var end = $(this).get(0).selectionEnd;
    $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end));

    $(this).get(0).selectionStart =
    $(this).get(0).selectionEnd = start + 1;
  }
});