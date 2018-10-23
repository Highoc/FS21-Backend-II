$(document).ready(
    function () {
        autoload = function() {
            $('.autoload').each(
                function () {
                    $(this).load($(this).data('url'));
                })
        };
        autoload();
        window.setInterval(autoload, 2000);

        $(document).on('click', '.addcommentbutton', function () {
            $('.ajax-add-comment').load($(this).data('url'));
            $('.ajax-add-comment').attr('action', $(this).data('url'));
        });

        $(document).on('submit', '.ajax-add-comment', function () {
            var form = this;
            $.post(
                $(form).attr('action'),
                $(form).serialize(),
                function (response) {
                    if (response == 'OK') {
                        autoload();
                        $('#myModal').modal('toggle');
                    } else {
                        $('.ajax-add-comment').replaceWith(response);
                    }
                }
            );
            return false;
        });

        $(document).on('submit', '.like-form', function () {
            var form = this;
            $.post(
                $(form).data('url'),
                $(form).serialize(),
                function (response) {
                    autoload();
                }
            );
            return false;
        });

        $('.selectmultiple').each( function () {
            $(this).attr('class', 'chosen-select');
        });

        $('.chosen-select').chosen();
    }
)