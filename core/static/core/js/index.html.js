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
    }).then(function () {
        subcategory.val(subcategory.data('selected')|| subcategory.val());
        subcategory.change();
        $('.selectpicker').selectpicker('refresh');
    });
    var category = $('#category');
    category.val(category.data('selected') || 1);
    category.selectpicker('refresh');
    category.change();
});