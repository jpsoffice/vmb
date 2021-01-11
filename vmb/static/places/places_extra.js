$ = $? $ : django.jQuery;
$(document).on('placeChanged', function (e, eventInfo) {
    let elem = $(eventInfo.element);
    const placeType = elem.attr('name').split('_')[0];
    let place = eventInfo.place;

    let city = state = "";

    if (place.address_components.length === 1) {
        city = state = place.address_components[0].long_name;
    } else {
        place.address_components.forEach(function(address, index) {
            if (address.types.includes('locality')) {
                city = address.long_name;
            } else if (address.types.includes('administrative_area_level_1')) {
                state = address.long_name;
            }
        });
    }
    $('input#id_' + placeType + '_city').val(city);
    $('input#id_' + placeType + '_state').val(state);
});