$(document).ready(function () {
    $('.favorite').click(function () {
        let fav_button = $(this)[0];
        let article_id = $(this).attr("data");
        $.get('/favorite_article/' + article_id + '/', function (is_favorited) {
            fav_button.classList.toggle('btn-danger');
            fav_button.classList.toggle('btn-primary');
            if (is_favorited === 'True') {
                fav_button.innerText = 'unfavorite';
            } else {
                fav_button.innerText = 'refavorite';
            }
        });
    });
});

