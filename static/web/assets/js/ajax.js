var isLoading = false;
$(document).on("submit", "form.ajax", function (e) {
    console.log('===================')
    e.preventDefault();
    var $this = $(this),
        data = new FormData(this),
        action_url = $this.attr("action"),
        reset = $this.hasClass("reset"),
        reload = $this.hasClass("reload"),
        redirect = $this.hasClass("redirect"),
        redirect_url = $this.attr("data-redirect");

    if (!isLoading) {
        isLoading = true;
        $.ajax({
            url: action_url,
            type: "POST",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            dataType: "json",
            success: function (data) {
                var status = data.status;
                var title = data.title;
                var message = data.message;
                var pk = data.pk;
                if (status == "true") {
                    title ? (title = title) : (title = "Success");
                    Swal.fire({
                        title: title,
                        html: message,
                        icon: "success",
                    }).then(function () {
                        redirect && (window.location.href = redirect_url), reload && window.location.reload(), reset && window.location.reset();
                    });
                } else {
                    title ? (title = title) : (title = "An Error Occurred");
                    Swal.fire({
                        title: title,
                        html: message,
                        icon: "error",
                    });
                }
            },
            error: function (data) {
                var title = "An error occurred",
                    message = "something went wrong";
                Swal.fire({
                    title: title,
                    html: message,
                    icon: "error",
                });
            },
        }).then(function (response) {
            isLoading = false;
        });
    }
});

