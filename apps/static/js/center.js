$(function () {
// 设置富文本
    tinymce.init({
        selector: '.mytextarea',
        height: 400,
        plugins: 'quickbars emoticons',
        inline: false,
        toolbar: true,
        menubar: true,
        quickbars_selection_toolbar: 'bold italic | link h2 h3 blockquote',
        quickbars_insert_toolbar: 'quickimage quicktable',

    });

    $('.right1').hide();
    // $('.right1').eq(0).show();
    $('.right1').first().show();
    $('#left p').first().css({'background-color': 'rgba(30, 150, 196, 0.94)'});
    //切换右侧div
    $('#left p').each(function (i) {
        $(this).click(function () {
            $('#left p').css({'background-color': 'rgba(30, 150, 196, 0.94)'});
            $(this).css({'background-color': 'skyblue', 'box-shadow': '5px 5px 5px deepskyblue'});
            $('.right1').hide();
            $('.right1').eq(i).show();
        });
    });
})