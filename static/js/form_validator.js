

$(document).ready(function () {
  // $("#date_pesquise, #data_p, #data, #data_venc").attr("maxlength",8).attr("minlength", 8)
  $('#data_venc, #date_pesquise_ini, #date_pesquise_fim').mask('00/00/0000');

  $("#preco_p, #preco, #preco_pesquise, #list_preco, #soma_filtro, #soma_home").mask('000.000,00', {reverse: true});
  
  var table = $('table');

   table.find('tr').each(function(indice){
      $(this).find('#list_h_td').each(function(indice){
       var status = $(this).text()
       if(status=='Pago'){
          $(this).css('background', '#90EE90')
       }
       else{
         $(this).css('background', '#FF6347')
       }
    });
});

 fetch('http://localhost:5000/venc')
 .then(function(response){
    return response.json()

 })
 .then(function(data){
   let a = Object.keys(data)
   a.forEach(function(k){
      alert(`Faturas que vencem hoje:\n ${data[k]}`)
   })
   });
    
   
   //called when key is pressed in textbox
    $("#preco_p, #data, #preco, #preco_p").keypress(function (e) {
       //if the letter is not digit then display error and don't type anything
       if(e.which != 8 && e.which != 0 && e.which != 46 && e.which !=44 && (e.which < 48 || e.which > 57)) {
          alert("somente Digitos!")
                 return false;
      }
     });

     


 
  

  });

 


