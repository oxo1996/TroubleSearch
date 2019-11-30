
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
$(document).ready(function(){
var productCount = 1;

$('select.select').each(function(){
            var title = $(this).attr('title');
            if( $('option:selected', this).val() != ''  ) title = $('option:selected',this).text();
            $(this)
                .css({'z-index':10,'opacity':0,'-khtml-appearance':'none'})
                .after('<span class="product">' + title + '</span>')
                .change(function(){
                    val = $('option:selected',this).text();
                    $(this).next().text(val);
                    })
        });




$("#plus").click(function () {
    var searchProduct = $('#product1').clone(true);
    searchProduct.children('#product').empty();
    searchProduct.children('#plus').remove();
    var productId = 'product'+String(++productCount);
    searchProduct.attr('id',productId);
    //searchProduct.children("#categories").attr("name","새로운네임")
    searchProduct.appendTo("#using");

});

$("#categories").on("change",dropdown);
$("#brand").on("change",dropdown);
function dropdown(){
    var parentProduct = $(this).closest("div").attr('id');
    var brandName = $("#"+parentProduct+" #brand option:selected").val();
    var categoriesName = $("#"+parentProduct+" #categories option:selected").val();
    
    $.ajax({
    method:"GET",
    url : "{% url 'ajax' %}",
    dataType:"json",
    data : {brand:brandName, categories:categoriesName},
    success:function(data){ 
        $( "#"+parentProduct+" #product" ).empty();
        for(var productName in data){          
        //$("#"+parentProduct+" #product").append("<option value="+"\'"+data[productName]+"\'"+">"+data[productName]+"</option>");
        $("#"+parentProduct+" #product").append("<option value=\""+data[productName]+"\">"+data[productName]+"</option>");
        }
    },
    error: function(request, status, error){
    alert("브랜드와 카테고리를 다시 설정해주세요!");
    }
        
    });

}


});