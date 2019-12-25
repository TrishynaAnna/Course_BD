$("button[name='btn_delete_group']").click(function() {

    var data = { group_id : $(this).data('group_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_group",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_group']").click(function() {

    window.location = "edit_group?group_id="+$(this).data('group_id');

});


$("button[name='btn_new_group']").click(function() {

    window.location = "new_group";

});

