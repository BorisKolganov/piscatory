/*
 * Chained - jQuery / Zepto chained selects plugin
 *
 * Copyright (c) 2010-2014 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.appelsiini.net/projects/chained
 *
 * Version: 1.0.0
 *
 */

;(function ($, window, document, undefined) {
    "use strict";

    $.fn.remoteChained = function (options) {
        var self = this;
        return new Promise(function (resolve, reject) {
            var settings = $.extend({}, $.fn.remoteChained.defaults, options);

            /* Loading text always clears the select. */
            if (settings.loading) {
                settings.clear = true;
            }
            self.each(function () {

                var request = false;
                /* Track xhr requests. */

                $(settings.parents).each(function () {
                    $(this).bind("change", function () {
                        var value = ($(this).is("select") ? $(":selected", this) : $(this)).val();

                        /* If previous request running, abort it. */
                        /* TODO: Probably should use Sinon to test this. */
                        if (request && $.isFunction(request.abort)) {
                            request.abort();
                            request = false;
                        }

                        if (settings.clear) {
                            if (settings.loading) {
                                /* Clear the select and show loading text. */
                                build.call(self, {"": settings.loading});
                            } else {
                                /* Clear the select. */
                                $("option", self).remove();
                            }

                            /* Force updating the children to clear too. */
                            $(self).trigger("change");
                        }

                        request = $.getJSON(settings.url + value + '/', function (json) {
                            build.call(self, json);
                            /* Force updating the children. */
                            $(self).trigger("change");
                            resolve();
                        });
                    });

                    /* If we have bootstrapped data given in options. */
                    if (settings.bootstrap) {
                        build.call(self, settings.bootstrap);
                        settings.bootstrap = null;
                    }
                });

                /* Build the select from given data. */
                function build(json) {
                    /* If select already had something selected, preserve it. */
                    var selected_key = $(":selected", self).val();

                    /* Clear the select. */
                    $("option", self).remove();
                    var option_list = [];
                    if ($.isArray(json)) {
                        if ($.isArray(json[0])) {
                            /* JSON is already an array of arrays. */
                            /* [["","--"],["series-1","1 series"],["series-3","3 series"]] */
                            option_list = json;
                        } else {
                            /* JSON is an array of objects. */
                            /* [{"":"--"},{"series-1":"1 series"},{"series-3":"3 series"}] */
                            option_list = $.map(json, function (value) {
                                return $.map(value, function (value, index) {
                                    return [[index, value]];
                                });
                            });
                        }
                    } else {
                        /* JSON is an JavaScript object. Rebuild it as an array. */
                        /* {"":"--","series-1":"1 series","series-3":"3 series"} */

                        for (var index in json) {
                            if (json.hasOwnProperty(index)) {
                                option_list.push([index, json[index]]);
                            }
                        }
                    }

                    /* Add new options from json. */
                    for (var i = 0; i !== option_list.length; i++) {
                        var key = option_list[i][0];
                        var value = option_list[i][1];

                        /* Set the selected option from JSON. */
                        if ("selected" === key) {
                            selected_key = value;
                            continue;
                        }
                        var option = $("<option />").val(key).append(value);
                        $(self).append(option);
                    }
                    $(self).selectpicker('refresh');

                    /* Loop option again to set selected. IE needed this... */
                    $(self).children().each(function () {
                        if ($(this).val() === selected_key + "") {
                            $(this).attr("selected", "selected");
                        }
                    });

                    /* If we have only the default value disable select. */
                    if (1 === $("option", self).size && $(self).val() === "") {
                        $(self).prop("disabled", true);
                    } else {
                        $(self).prop("disabled", false);
                    }
                }
            });
        })

    };

    /* Alias for those who like to use more English like syntax. */
    $.fn.remoteChainedTo = $.fn.remoteChained;

    /* Default settings for plugin. */
    $.fn.remoteChained.defaults = {
        attribute: "name",
        depends: null,
        bootstrap: null,
        loading: null,
        clear: false
    };

})(window.jQuery || window.Zepto, window, document);