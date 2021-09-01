function index(){
    $.ajax({
        url:"/rectores/postulantes/index/",
        type:"get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#example')){
                $('#example').DataTable().destroy();
            }
            $('#example tbody').html("");
            for(let i = 0;i < response.length;i++){
                let fila = '<tr>';
                fila += '<td>' + (i +1 ) + '</td>';
                fila += '<td>' + response[i]["fields"]['nombre'] ['apellido_p'] ['apellido_m']+ '</td>';
                fila += '<td>' + response[i]["fields"]['cargo'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nivel_ingles'] + '</td>';
                fila += '<td>' + response[i]["fields"]['titulo'] + '</td>';
                fila += '<td>' + response[i]["fields"]['cv.url'] + '</td>';
                fila += '<td>' +  + '</td>';
                fila += '<td>' +  + '</td>';
                fila += '<td>' +  + '</td>';
                fila += '</tr>';
                $('#example tbody').append(fila);
            }
        }
    })
}