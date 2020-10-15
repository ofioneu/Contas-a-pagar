

$(document).ready(function () {
  // $("#date_pesquise, #data_p, #data, #data_venc").attr("maxlength",8).attr("minlength", 8)
  $('#data_venc, #date_pesquise_ini, #date_pesquise_fim').mask('00/00/0000');

  $("#preco_p, #preco, #preco_pesquise, #list_preco, #soma_filtro, #soma_home").mask('000.000,00', {reverse: true});
  
  $("#list_h").each(function(){
     var a=$('tr').length
    console.log(a)

  })
  
   //called when key is pressed in textbox
    $("#preco_p, #data, #preco, #preco_p").keypress(function (e) {
       //if the letter is not digit then display error and don't type anything
       if(e.which != 8 && e.which != 0 && e.which != 46 && e.which !=44 && (e.which < 48 || e.which > 57)) {
          alert("somente Digitos!")
                 return false;
      }
     });

     


 
  

  });

 


