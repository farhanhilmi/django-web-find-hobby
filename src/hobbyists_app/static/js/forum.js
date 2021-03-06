$(function () {
    var loadForm = function () {
        var btn = $(this);
        console.log("LOAD FORM")
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-forum .modal-content").html("");
                $("#modal-forum").modal("show");
                console.log("BEFORESEND");

            },
            success: function (data) {
                $("#modal-forum .modal-content").html(data.html_form);

            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    location.reload();
                    $(".list-forum-data .card-deck").html(data.html_list_forum);
                    $("#modal-forum").modal("hide");
                    console.log("REFRESH");
                    // window.location.href = "http://www.w3schools.com";
                    // $(document).ajaxStop(function () {
                    //     window.location.reload();
                    // });
                }
                else {
                    $("#modal-forum .modal-content").html(data.html_form);
                    console.log("REFRESH RIDAK");
                }
            }
        });
        return false;
    };

    // Update task
    $(".btnForumEdit").on("click", loadForm);
    $("#modal-forum").on("submit", ".upadeteforumForm", saveForm);
});

