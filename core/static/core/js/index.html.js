/**
 * Created by Boris on 05.02.17.
 */
$(document).ready(function () {
    var category = $('#category');
    var subcategory = $('#subcategory');
    var showButton = $('.show-button');

    subcategory.remoteChained({
        parents: "#category",
        url : "/adverts/get_subcategories/",
        loading : "Загрузка"
    }).then(function () {
        subcategory.val(subcategory.data('selected'));
        subcategory.change();
        $('.selectpicker').selectpicker('refresh');
    });

    showButton.on('click', function () {
        var hrefTemplate = undefined;
        if (+subcategory.val()) {
            hrefTemplate = $(this).data('href-subcategory-template');
            hrefTemplate = hrefTemplate.replace('/0/', '/' + category.val() + '/');
            hrefTemplate = hrefTemplate.replace('/0/', '/' + subcategory.val() + '/');
            $(this).attr('href', hrefTemplate);
        } else if (+category.val()) {
            hrefTemplate = $(this).data('href-category-template');
            hrefTemplate = hrefTemplate.replace('/0/', '/' + category.val() + '/');
            $(this).attr('href', hrefTemplate);
        } else {
            $(this).attr('href', $(this).data('href-all'));
        }
    });
    category.val(category.data('selected'));
    category.selectpicker('refresh');
    category.change();
});