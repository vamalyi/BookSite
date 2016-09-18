/**
 * Created by freeday on 04.03.16.
 */
;
(function () {

    var delivery = $('select[name$=delivery]');
    var city = $('select#select_city');
    var warehouse = $('select#select_warehouses');

    delivery.on('change', function () {
        var t = $(this);
        var city = t.closest('form').find('select#select_city');
        var warehouses = t.closest('form').find('select#select_warehouses');
        var address = t.closest('form').find('[name$=shipping_address]');
        if (this.value == 'nova_poshta') {
            warehouses.prop('required', true);
            city.prop('required', true);
            $.get('/api/cities/', function (data) {
                var option;
                var data_json = data['data'];
                city.html(
                    '<option value="">Оберіть місто</option>');
                for (var m = 0; m < data_json.length; m++) {
                    option = data_json[m];
                    option = {
                        'value': option['code'],
                        'label': option['city']
                    };
                    city.append(createOption(option));
                }
                city.removeClass('hidden');
                city.prop('disabled', false);

                t.closest('form').find('[name$=delivery_warehouses]').val('');
                warehouses.html('<option value="">Оберіть відділення</option>');
                warehouses.addClass('hidden');
                warehouses.prop('disabled', true);
            });
        } else {
            warehouses.prop('required', false);
            city.prop('required', false);

            t.closest('form').find('[name$=delivery_city]').val('');
            city.html('<option value="">Оберіть місто</option>');
            city.addClass('hidden');
            city.prop('disabled', true);

            t.closest('form').find('[name$=delivery_warehouses]').val('');
            warehouses.html('<option value="">Оберіть відділення</option>');
            warehouses.addClass('hidden');
            warehouses.prop('disabled', true);
        }

        if (this.value == 'city') {
            address.removeClass('hidden');
        } else {
            address.addClass('hidden');
        }
    });

    city.on('change', function () {
        var t = $(this);
        var city_field = t.closest('form').find('[name$=delivery_city]');
        var warehouses_field = t.closest('form').find('[name$=delivery_warehouses]');
        var warehouses = t.closest('form').find('select#select_warehouses');
        city_field.val(t[0].options[t[0].selectedIndex].label);
        warehouses_field.val('');
        $.get('/api/warehouses/' + t.val(), function (data) {
            var option;
            var data_json = data['data'];
            warehouses.html(
                '<option value="">Оберіть відділення</option>');
            for (var m = 0; m < data_json.length; m++) {
                option = data_json[m];
                option = {
                    'value': option['code'],
                    'label': option['city']
                };
                warehouses.append(createOption(option));
            }
            warehouses.removeClass('hidden');
            warehouses.prop('disabled', false);
        });
    });

    warehouse.on('change', function () {
        var t = $(this);
        var warehouses_field = t.closest('form').find('[name$=delivery_warehouses]');
        warehouses_field.val(t[0].options[t[0].selectedIndex].label);
    });
    function createOption(optionData) {
        var option = document.createElement('option');
        option.value = optionData.value;
        option.innerHTML = optionData.label;
        option.label = optionData.label;
        return option
    }
}).call(this);
