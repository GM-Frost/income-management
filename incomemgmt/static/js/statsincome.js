const renderChart = (data,labels)=>{
    const ctx = document.getElementById('myChart2').getContext("2d");
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months Income',
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
        responsive: true,
        plugins: {
          title: {
              display: true,
              text: 'Income Per Source',
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
      type: 'polarArea',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months Income',
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
        responsive: true,
        plugins: {
          legend: {
                position: 'top',
                },
          title: {
              display: true,
              text: 'Income Per Source',
          },
      },
        scales: {
            y: {
                // the data minimum used for determining the ticks is Math.min(dataMin, suggestedMin)
                suggestedMin: 30,
        
                // the data maximum used for determining the ticks is Math.max(dataMax, suggestedMax)
                suggestedMax: 50,
              }
        }
      }
    }); 

  };
  
  
  const getChartData=()=>{
  
    fetch("income_source_summary")
    .then((res)=>res.json())
    .then((results)=>{
      const category_data = results.income_source_data;
      const [labels,data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      renderChart(data,labels);
    });
  
  };
  document.onload=getChartData();
  