const renderChart = (data,labels)=>{
  
  const ctx = document.getElementById('myChart2').getContext("2d");
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: 'Last 6 months Expenses',
        data: data,
        borderWidth: 1,
      }]
    },
    options: {
      plugins: {
        title: {
            display: true,
            text: 'Expense Per Category',
        }
    },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  const ctx2 = document.getElementById('myChart1').getContext("2d");
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Last 6 months Expenses',
        data: data,
        borderWidth: 1,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(75, 192, 192)',
          'rgb(255, 205, 86)',
          'rgb(201, 203, 207)',
          'rgb(54, 162, 235)'
          ]
      }]
    },
    options: {
      plugins: {
        title: {
            display: true,
            text: 'Expense Per Category',
        }
    },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

};

const getChartData=()=>{

  fetch("/expense_category_summary")
  .then((res)=>res.json())
  .then((results)=>{
    const category_data = results.expense_category_data;
    const [labels,data] = [
      Object.keys(category_data),
      Object.values(category_data),
    ];
    renderChart(data,labels);
  });

};
document.onload=getChartData();
