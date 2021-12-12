var app = angular.module('myApp', ['ngAnimate']);

app.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
   }]);

var o = {
 'a': 3, 'b': 4,
 'doStuff': function() {
   alert(this.a + this.b);
 }
};
// o.doStuff(); // displays: 7
const NamedStruct = (name, ...keys) => ((...v) => keys.reduce((o, k, i) => {o[k] = v[i]; return o} , {_name: name}))
const Item = NamedStruct('Item', 'id', 'speaker', 'country')
var myItems = [
    Item(1, 'john', 'au'),
    Item(2, 'mary', 'us')
];
class Reference {
    /**
     * @constructs Reference
     * @param {Object} p The properties.
     * @param {String} p.class The class name.
     * @param {String} p.field The field name.
     */
    constructor(p={}) {
        this.class = p.class;
        this.field = p.field;
    }
}

function getData2() {
  /* $.get( "ajax/test.html", function( data ) {
    $( ".result" ).html( data );
  }); */
}

function getJsonData(myUrl) {
  var geojson;
  var jqxhr = $.get( myUrl, function(data) {
    // console.log( "success data xhr", data );
    geojson = data;
  })
    .done(function(data) {
      // console.log( "xhr closed" );
      geojson= JSON.parse(data);
      console.log( "Readed ", geojson);
    })
    .fail(function() {
      // console.log( "xhr call error" );
    })
    .always(function() {
      // console.log( "xhr call finished" );
    });
  // Perform other work here ...
  return geojson;

  jqxhr.always(function() {
    // console.log( "xhr reading second finished" );
  });
}

let lists = function(data) { this.title = data.title; };
app.controller('SuperListController', ['$sope', '$timeout', function($scope, $timeout){
    var series = getJsonData("/api/fetch");
    $scope.title = 'Second step at Angular data!';
    $scope.otherlist = new Array();
    $scope['series'] = new Array();
    console.log(typeof(series));
    $scope.series.push(series);
    //$scope.$eval();
    $scope.mainList = function(){
      var jsonString = '{"some":"json"}';
      var d = JSON.parse(jsonString);
      // $scope.Profiles.push(d);
      // var jsonPretty = JSON.stringify(d,null,2);
    };

    $timeout(function(){
      let jsonData = '[{"title": "hello World"}]';
      // var jsonData = [{title: 'hello World'}];
      // var somedata = JSON.parse(jsonData);
      let description = {title: "title2"}
      $scope.otherlist.push(description);
      //$scope.otherlist = series;
      //$scope.otherlist = [{title: jsonDataOnline.title, series: jsonDataOnline.series}];
      // console.log(d) == console.log($scope.list);
      //return $scope;
    }, 500);

  }]);

  app.controller('AnimateController', ['$scope', '$timeout', function($scope, $timeout){
      $scope.title = 'First Step at Angular Animations!';
      $scope.addToList = function(){ $scope.list.push({title: $scope.listElement}); };
      $timeout(function(){
        $scope.list = [
          {title: 'hello World'},
          {title: 'hello World'}
        ];
      }, 100);

    }]);
