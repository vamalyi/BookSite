/**
 * Created by pluton on 10.03.16.
 */

;
(function () {
    var product_on_page_12 = document.getElementById('product_on_page_12');
    var product_on_page_24 = document.getElementById('product_on_page_24');
    var product_on_page_48 = document.getElementById('product_on_page_48');
    var product_on_page_all = document.getElementById('product_on_page_all');

    if (product_on_page_12) {
        product_on_page_12.onclick = function(){
            var options = {
                'path': '/',
                'expires': 360000
            };
            setCookie('product_on_page', 12, options);
            location.reload();
        };
    }
    if (product_on_page_24) {
        product_on_page_24.onclick = function(){
            var options = {
                'path': '/',
                'expires': 360000
            };
            setCookie('product_on_page', 24, options);
            location.reload();
        };
    }
    if (product_on_page_48) {
        product_on_page_48.onclick = function(){
            var options = {
                'path': '/',
                'expires': 360000
            };
            setCookie('product_on_page', 48, options);
            location.reload();
        };
    }
    if (product_on_page_all) {
        product_on_page_all.onclick = function(){
            var options = {
                'path': '/',
                'expires': 360000
            };
            setCookie('product_on_page', 'all', options);
            location.reload();
        };
    }

    function setCookie(name, value, options) {
        options = options || {};

        var expires = options.expires;

        if (typeof expires == "number" && expires) {
            var d = new Date();
            d.setTime(d.getTime() + expires * 1000);
            expires = options.expires = d;
        }
        if (expires && expires.toUTCString) {
            options.expires = expires.toUTCString();
        }

        value = encodeURIComponent(value);

        var updatedCookie = name + "=" + value;

        for (var propName in options) {
            updatedCookie += "; " + propName;
            var propValue = options[propName];
            if (propValue !== true) {
                updatedCookie += "=" + propValue;
            }
        }

        document.cookie = updatedCookie;
    }
}).call(this);
