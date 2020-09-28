

$(document).ready(function () {
   $("#date_pesquise").attr("maxlength",8)
    //called when key is pressed in textbox
    $("#preco, #preco_p, #data, #data_p").keypress(function (e) {
       //if the letter is not digit then display error and don't type anything
       if (e.which != 8 && e.which != 0 && e.which != 46 && (e.which < 48 || e.which > 57)) {
          //display error message
          $("#errmsg").html("Somente digitos").show().fadeOut("slow");
                 return false;
      }
     });
  

  });

 


