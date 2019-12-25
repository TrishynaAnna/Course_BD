$("button[name='btn_delete_gpoupuser']").click(function() {

    var data = { user_id : $(this).data('user_id'),group_id : $(this).data('group_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_gpoupuser",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});



$("button[name='btn_new_gpoupuser']").click(function() {

    window.location = "new_gpoupuser";

});

