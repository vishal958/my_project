jQuery(document).ready(function () {
    $('.likebutton.like-dislike').click(function () {
        var catid;
        catid = $(this).attr("data-catid");
        var preference = parseInt($(this).attr("data-preference"));
        var like = parseInt($('.like').text())
        var dislike = parseInt($('.dislike').text())
        $.ajax({
            type: "GET",
            url: "/likepost",
            data: {
                post_id: catid,
                userpreference: 1
            },
            success: function (data) {
                if (preference == 1) {
                    $('.like').text(like - 1);
                    $('.like-dislike').attr("data-preference", '0');
                    $('#message').text('');

                } else if (preference == 2) {

                    $('.dislike').text(dislike - 1);
                    $('.like').text(like + 1);
                    $('.like-dislike').attr("data-preference", '1');
                    $('#message').html('Thank you very much for liking my Post &#128525;');
                    $('#message').css('color', 'green');
                } else {
                    $('.like').text(like + 1);
                    $('.like-dislike').attr("data-preference", '1');
                    $('#message').html('Thank you very much for liking my Post &#128525;');
                    $('#message').css('color', 'green');
                }
            }
        })

    });
    $('.dlikebutton.like-dislike').click(function () {

        var catid;
        catid = $(this).attr("data-catid");
        var preference = parseInt($(this).attr("data-preference"));
        var like = parseInt($('.like').text())
        var dislike = parseInt($('.dislike').text())
        $.ajax({
            type: "GET",
            url: "/likepost",
            data: {
                post_id: catid,
                userpreference: 2
            },
            success: function (data) {
                if (preference == 1) {
                    $('.like').text(like - 1);
                    $('.like-dislike').attr("data-preference", '2');
                    $('.dislike').text(dislike + 1);
                    $('#message').html('Please provide some comments so that I can give you better next time &#128528;');
                    $('#message').css('color', 'red');

                } else if (preference == 2) {

                    $('.dislike').text(dislike - 1);
                    $('.like-dislike').attr("data-preference", '0');
                    $('#message').text('');
                } else {
                    $('.dislike').text(dislike + 1);
                    $('.like-dislike').attr("data-preference", '2');
                    $('#message').html('Please provide some comments so that I can give you better next time &#128528;');
                    $('#message').css('color', 'red');
                }
            }
        })

    });
});