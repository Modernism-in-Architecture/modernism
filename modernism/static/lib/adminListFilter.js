function initializeCityFilter() {
    $(document).ready(function() {

        var searchParams = new URLSearchParams(window.location.search);
        var cityId = searchParams.get('city_id');
    
        if (cityId) {
          $("#id_city").val(`?city_id=${cityId}`).trigger('change');
        }
    
        $("#id_city").select2().on('select2:select', function (e) {
          var selectedOptionParam = e.params.data.id;
          var cityId = selectedOptionParam.split('=')[1];
          var searchParams = new URLSearchParams(window.location.search);
          cityId ? searchParams.set('city_id', cityId) : searchParams.delete('city_id');
          window.location.search = searchParams.toString();
          
        });
      });
}

function initializeCountryFilter() {
    $(document).ready(function() {

        var searchParams = new URLSearchParams(window.location.search);
        var countryId = searchParams.get('country_id');
    
        if (countryId) {
          $("#id_country").val(`?country_id=${countryId}`).trigger('change');
        }
    
        $("#id_country").select2().on('select2:select', function (e) {
          var selectedOptionParam = e.params.data.id;
          var countryId = selectedOptionParam.split('=')[1];
          var searchParams = new URLSearchParams(window.location.search);
          countryId ? searchParams.set('country_id', countryId) : searchParams.delete('country_id');
          window.location.search = searchParams.toString();
          
        });
      });
}
