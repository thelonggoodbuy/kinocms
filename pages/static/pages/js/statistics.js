/* global Chart:false */

$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode = 'index'
  var intersect = true

  var $salesChart = $('#sales-chart')
  var salesChart = new Chart($salesChart, {
    type: 'bar',
    data: {
      labels: ['JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
      datasets: [
        {
          backgroundColor: '#007bff',
          borderColor: '#007bff',
          data: [1000, 2000, 3000, 2500, 2700, 2500, 3000]
        },
        {
          backgroundColor: '#ced4da',
          borderColor: '#ced4da',
          data: [700, 1700, 2700, 2000, 1800, 1500, 2000]
        }
      ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks: $.extend({
            beginAtZero: true,

            callback: function (value) {
              if (value >= 1000) {
                value /= 1000
                value += 'k'
              }

              return '$' + value
            }
          }, ticksStyle)
        }],
        xAxes: [{
          display: true,
          gridLines: {
            display: false
          },
          ticks: ticksStyle
        }]
      }
    }
  })

  var date_of_seance = JSON.parse(document.getElementById('date_data').textContent)
  var date_of_show = JSON.parse(document.getElementById('date_of_show').textContent)

  

  var $visitorsChart = $('#visitors-chart')
  var visitorsChart = new Chart($visitorsChart, {
    data: {
      labels: date_of_show,
      datasets: [{
        type: 'line',
        data: [15, 120, 188, 20, 10, 177, 160],
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        pointBorderColor: '#007bff',
        pointBackgroundColor: '#007bff',
        fill: false
      },
      {
        type: 'line',
        data: [100, 80, 170, 67, 40, 77, 10],
        backgroundColor: 'tansparent',
        borderColor: '#ffc107',
        pointBorderColor: '#ffc107',
        pointBackgroundColor: '#ffc107',
        fill: false
      },
      {
        type: 'line',
        data: [160, 33, 22, 22, 80, 11, 100],
        backgroundColor: 'tansparent',
        borderColor: '#28a745',
        pointBorderColor: '#28a745',
        pointBackgroundColor: '#28a745',
        fill: false
      },
      {
        type: 'line',
        data: [11, 80, 170, 55, 180, 77, 55],
        backgroundColor: 'tansparent',
        borderColor: '#17a2b8',
        pointBorderColor: '#17a2b8',
        pointBackgroundColor: '#17a2b8',
        fill: false
      },
    ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks: $.extend({
            beginAtZero: true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display: true,
          gridLines: {
            display: false
          },
          ticks: ticksStyle
        }]
      }
    }
  })

});

// lgtm [js/unused-local-variable]
