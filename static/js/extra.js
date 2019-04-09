$(document).on('click', '.load', function(e){
  var url = ($(this).attr('data-url'));
  load(url);
});


function load(url){
  $('#ModalGeneral .modal-content').load(url, function (response, status, xhr) {
    if(status == "error"){
      if (xhr.status === 0){
        $('#ModalGeneral').modal('show');
        $('#ModalGeneral .modal-body').text('Холболтын алдаа. Сүлжээгээ шалгана уу.');
      }
      else if (xhr.status == 404) {
        $('#ModalGeneral').modal('show');
        $('#ModalGeneral .modal-body').html('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
      }
      else if (xhr.status == 500) {
        $('#ModalGeneral').modal('show');
        $('#ModalGeneral .modal-body').html('Алдаа 500. Серверийн дотоод алдаа.');
      }
      else if (xhr.status == 403) {
        $('#ModalGeneral').modal('show');
        $('#ModalGeneral .modal-body').html('Алдаа 403. Хандах эрх олгогдоогүй байна.');
      }
      else {
        $('#ModalGeneral').modal('show');
        $('#ModalGeneral .modal-body').html('Тодорхойгүй');
        console.log(response);
        console.log(status);
        console.log(xhr.status);
      }
    }
    else
    {
      $('#ModalGeneral').modal('show');
    }
  });
}


function SubmitForm(form_id){
  $(form_id).submit(function (e) {
    e.preventDefault();
    $(':submit').attr('disabled', 'disabled');
    $(form_id).data('submitted', true);
    var data = new FormData($(this).get(0));
    $.ajax({
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      data: data,
      cache: false,
      contentType: false,
      processData: false,
      success: function (xhr, ajaxOptions, thrownError) {
        if ( $(xhr).find('.has-error').length > 0 ) {
          $('#ModalGeneral').html(xhr);
          $(':submit').prop('disabled', false);
        }
        else if ( $(xhr).find('.alert-danger').length > 0 ) {
          $('#ModalGeneral').html(xhr);
          $('#ModalGeneral form').attr('action', action);
          $(':submit').prop('disabled', false);
        }
        else{
        }
      },
      error: function (xhr, ajaxOptions, thrownError) {
        $(form_id).data('submitted', false);
        $('#ModalGeneral').modal('hide');
        $.notify(
        {
          message: 'Та дахин оролдож үзнэ үү!',
          icon: 'glyphicon glyphicon-warning-sign',
          title: 'Системд алдаа гарлаа.',
        },
        {
          type: 'danger',
          placement: {
            from: "top",
            align: "right"
          },
        }
        );
      }
    });
  });
}