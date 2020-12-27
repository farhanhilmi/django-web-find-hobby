$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-tasks .modal-content").html("");
                $("#modal-tasks").modal("show");

            },
            success: function (data) {
                $("#modal-tasks .modal-content").html(data.html_form);
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
                    $("#data-forum").html(data.html_list_forum);

                    alertify.set('notifier', 'position', 'top-right');
                    alertify.notify('Aksi Berhasil!', 'success', 5)
                }
                else {
                    console.log("GAGAL")
                }
            }
        });
        return false;
    };

    // Create task
    $(".js-create-tugas").click(loadForm);
    $("#modal-tasks").on("submit", ".js-tugas-create-form", saveForm);

    // Update task
    $("#data-forum").on("click", ".js-update-forum", loadForm);
    $("#data-forum form").on("submit", ".js-forum-update-form", saveForm);

    // Delete task
    $("#data-forum").on("click", ".js-delete-tugas", loadForm);
    $("#modal-tasks").on("submit", ".js-tugas-delete-form", saveForm);

});

