angular.module('iLifeApp')

.directive('datepicker', function() {
    return {
        restrict: 'A',
        link: function() {
           $('.form_datetime').datetimepicker({
               weekStart: 1,
               todayBtn:  1,
               autoclose: 1,
               todayHighlight: 1,
               startView: 2,
               forceParse: 0,
               showMeridian: 1,
               format: "yyyy-mm-dd",
               minView: 2
           });
        }
    };
})

// .directive('imgCenter', function() {
//     return {
//         restrict: 'A',
//         link: function() {
//             $("[class^='img_']").css('marginTop', (-1 * this.clientHeight/2) + 'px');
//         }
//     };
// })

.directive('dropdown', function() {
    return {
        restrict: 'A',
        link: function() {
            $(".dropdown-toggle").dropdown();
        }
    };
});
