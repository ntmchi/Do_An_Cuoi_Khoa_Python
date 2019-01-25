function remove_unicode(unicode_string) {
    var str = unicode_string;
    str = str.toLowerCase();
    str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g,"a"); 
    str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g,"e"); 
    str = str.replace(/ì|í|ị|ỉ|ĩ/g,"i"); 
    str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g,"o"); 
    str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g,"u"); 
    str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g,"y"); 
    str = str.replace(/đ/g,"d");
    str = str.replace(/!|@|%|\^|\*|\(|\)|\+|\=|\<|\>|\?|\/|,|\.|\:|\;|\'|\"|\&|\#|\[|\]|~|\$|_|`|-|{|}|\||\\/g," ");
    str = str.replace(/ + /g," ");
    str = str.trim(); 
    return str;
}

var location_href = document.location.hash;    

if (location_href != '') {
    location_href = location_href.substr(1);
    var filterValue = $('#' + location_href).data('filter');
    $('.isotope-grid').isotope({filter: filterValue});
}

$('.sub-menu:eq(0) li a').on('click', function(e) {    
    var sub_href = $(this).data('id');
    var sub_filterValue = $('#' + sub_href).data('filter');
    $('.isotope-grid').isotope({filter: sub_filterValue});
});

$('.bread-crumb a:eq(1)').on('click', function(e){
    var sub1_filterValue = $(this).data('filter');
    $('.isotope-grid').isotope({filter: sub1_filterValue});
});

$('.thong-tin-cua-hang:eq(0)').show();

$(function () {
    $("#myList div").slice(0, 1).show();
    $("#Th_Load_more").on('click', function (e) {
        e.preventDefault();
        $("#myList div:hidden").slice(0, 4).slideDown();
        if ($("#myList div:hidden").length == 0) {
            $("#load").fadeOut('slow');
        }
        $('html,body').animate({
            scrollTop: $(this).offset().top
        }, 1500);
    });
});

$('.js-addcart-detail').on('click', function(e){
    var data = {        
        Ten_san_pham: $(this).parent().parent().parent().parent().find('h4').text(),
        // Ma_san_pham: $('input[name=Th_Ma_so]').val(),
        Ma_san_pham: $(this).parent().find('input[name=Th_Ma_so]').val(),
        So_luong: $(this).parent().find('.num-product').val(),
        Mau_sac: $(this).parent().parent().parent().find('.mau-sac').val(),
        Size: $(this).parent().parent().parent().find('.ma-size').val(),
        Hinh: $(this).parent().parent().parent().parent().parent().parent().find('.slick-active img:eq(0)').attr('src'),
        // Don_gia: $('input[name=Th_Don_gia]').val()
        Don_gia: $(this).parent().find('input[name=Th_Don_gia]').val(),
    };
    $.ajax({
        url: "/add-to-cart",
        method: "POST", 
        data: {
            item : JSON.stringify(data)
        },
        xhrFields: {
            withCredentials: true
        },
        success: function(result){  
            Th_Gio_hang.setAttribute('data-notify', result.len)
            Th_Gio_hang_M.setAttribute('data-notify', result.len) 
            $('.header-cart').html(result.html)        
          
        }
    });
});
$(document).on('click', '.js-hide-cart', function(){
    $('.js-panel-cart').removeClass('show-header-cart');
});

$('#dang-nhap').on('click',function(e){
    e.preventDefault();    
    $('#modal-dang-nhap').addClass('show-modal1');
});

$('.btn-dang-nhap').on('click',function(e){
    var data = {
        email: $('#email').val(),
        password: $('#password').val(),
    };
    $.ajax({
        url: "/nguoi-dung/dang-nhap",
        method: "POST", 
        data: {
            item : JSON.stringify(data)
        },
        xhrFields: {
            withCredentials: true
        },
        success: function(result){    
            if (result.status) {
                location.reload()
            } else {
                
            }                    
        }
    });
});