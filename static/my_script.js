// CHARTS

var emotionsOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Emotions',
                       fontSize: 20}
};





let ctx_donut = $("#emotionsChart").get(0).getContext("2d");

//Data and chart creation

$.get('/emotions_data.json', function(data){
    let myDonutChart = new Chart(ctx_donut, {
                                              type: 'doughnut',
                                              data: data,
                                              options: emotionsOptions
                                            });
      // $('#emotionLegend').html(myDonutChart.generateLegend());
});


