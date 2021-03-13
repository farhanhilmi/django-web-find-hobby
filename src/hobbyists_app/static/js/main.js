$(document).ready(function () {
  // forumDelVal = $('#delForumVal');
  $(".btnForumDelete").click(function () {
    $("#delForumVal").text($(this).data("one"));
    $("#delForumId").val($(this).data("id"));
  });

  $(".btnCommentDel").click(function () {
    $("#delCommentId").val($(this).data("id"));
    console.log("kaka");
  });

  $(".pwdChange").on("change paste keyup", function () {
    console.log("lala");
  });

  // $('.btnForumEdit').click(function () {
  //     $('#topicVal').val($(this).data('one'));
  //     $('#editForumId').val($(this).data('id'));
  // });

  // $('.btnForumEdit').click(function () {
  //     // var saccountCode = $("select#accountcombo").val();
  //     // var stringAccountCode = saccountCode.toString()
  //     // console.log("Account is: " + stringAccountCode);
  //     // console.log("YES MASUK");
  //     // var myURL = "ist-forum";
  //     // $.ajax({
  //     //     url: myURL,
  //     //     type: "POST",
  //     //     data: {
  //     //         "accountCode": "stringAccountCode"
  //     //     },
  //     //     dataType: "text",
  //     // })
  //     // document.location.hash = "?show_picture";
  //     // var encodedState = base64(json(state));
  //     // var newLocation = oldLocationWithoutFragment + "#" + encodedState;
  //     // let forumID = $(this).data('id');
  //     // let myUrl = "list-forum?id=" + forumID;
  //     // window.history.pushState("object", "Title", myUrl);

  //     parent.location.hash = "hello";
  // });
});
