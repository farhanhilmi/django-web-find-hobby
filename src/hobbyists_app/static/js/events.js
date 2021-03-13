// $(function () {
//   var loadForm = function () {
//     var btn = $(this);
//     $.ajax({
//       url: btn.attr("data-url"),
//       type: "get",
//       dataType: "json",
//       beforeSend: function () {
//         $("#modal-event .modal-content").html("");
//         $("#modal-event").modal("show");
//         print("asasasJAJA");
//       },
//       success: function (data) {
//         $("#modal-event .modal-content").html(data.html_form);
//       },
//     });
//   };

//   var saveForm = function () {
//     var form = $(this);
//     $.ajax({
//       url: form.attr("action"),
//       data: form.serialize(),
//       type: form.attr("method"),
//       dataType: "json",
//       success: function (data) {
//         if (data.form_is_valid) {
//           $(".list-event-data .card-deck").html(data.html_list_event);
//           $("#modal-event").modal("hide");
//           console.log("REFRESH");
//           // window.location.href = "http://www.w3schools.com";
//           // $(document).ajaxStop(function () {
//           //     window.location.reload();
//           // });
//         } else {
//           $("#modal-event .card-body").html(data.html_form);
//           console.log("REFRESH RIDAK");
//         }
//       },
//     });
//     return false;
//   };

//   // Update task
//   $(".btnEventEdit").on("click", loadForm);
//   $("#modal-event").on("submit", ".upadeteEventForm", saveForm);
// });
