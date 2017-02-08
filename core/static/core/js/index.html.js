/**
 * Created by Boris on 05.02.17.
 */
$(document).ready(function () {
    var subcategory = $('#subcategory');
    subcategory.on('change', function () {
        var subcategoryButton = $('.show-subcategory');
        var hrefTemplate = subcategoryButton.data('href-template');
        subcategoryButton.attr('href', hrefTemplate.replace('0', $(this).val()));
    });
    subcategory.remoteChained({
        parents: "#category",
        url : "/adverts/get_subcategories/",
        loading : "Загрузка"
    }, function () {
        subcategory.val(subcategory.data('selected'));
        subcategory.change();
        $('.selectpicker').selectpicker('refresh');
    });
    var category = $('#category');
    category.val(category.data('selected'));
    category.selectpicker('refresh');
    category.change();
});