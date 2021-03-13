$(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-forum .modal-content").html("");
        $("#modal-forum").modal("show");
      },
      success: function (data) {
        $("#modal-forum .modal-content").html(data.html_form);
      },
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $(".list-comment-data .card-deck").html(data.html_list_comment);
          $("#modal-forum").modal("hide");
          console.log("REFRESH");
          // window.location.href = "http://www.w3schools.com";
          // $(document).ajaxStop(function () {
          //     window.location.reload();
          // });
        } else {
          $("#modal-forum .card-body").html(data.html_form);
          console.log("REFRESH RIDAK");
        }
      },
    });
    return false;
  };

  // Update task
  $(".btnCommentEdit").on("click", loadForm);
  $("#modal-forum").on("submit", ".upadeteCommentForm", saveForm);
});
