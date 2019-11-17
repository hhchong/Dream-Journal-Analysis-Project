// CHARTS

var emotionsOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Emotions',
                       fontSize: 20}
};

var charactersOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Characters',
                       fontSize: 20}
};

var themesOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Themes',
                       fontSize: 20}
};

var settingsOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Settings',
                       fontSize: 20}
};



let ctx_donut = $("#emotionsChart").get(0).getContext("2d");
let ctx_donut = $("#charactersChart").get(0).getContext("2d");
let ctx_donut = $("#themesChart").get(0).getContext("2d");
let ctx_donut = $("#settingsChart").get(0).getContext("2d");

//Data and chart creation


$.get('/emotions_data.json', function(data){
    let myDonutChart = new Chart(ctx_donut, {
                                              type: 'doughnut',
                                              data: data,
                                              options: emotionsOptions
                                            });
});

$.get('/characters_data.json', function(data){
    let myDonutChart = new Chart(ctx_donut, {
                                              type: 'doughnut',
                                              data: data,
                                              options: charactersOptions
                                            });
});

$.get('/themes_data.json', function(data){
    let myDonutChart = new Chart(ctx_donut, {
                                              type: 'doughnut',
                                              data: data,
                                              options: themesOptions
                                            });
});

$.get('/settings_data.json', function(data){
    let myDonutChart = new Chart(ctx_donut, {
                                              type: 'doughnut',
                                              data: data,
                                              options: settingsOptions
                                            });
});


